'''
Description: 获取 arXiv 论文作者单位
Version: 1.0
Author: Glenn
Email: chenluda01@outlook.com
Date: 2023-04-24 15:32:39
FilePath: getAffiliation.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import os
import re
from io import BytesIO

import openai
import pdfplumber
import requests
import spacy
from transformers import pipeline

# 设置 OpenAI 的 API key
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_affiliation_by_bert(text):
    """
    使用 bert 模型获取作者单位
    """
    # 初始化 BERT NER
    nlp = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER")
    entities = nlp(text)

    institutions = set()
    # 提取组织实体
    for i, entity in enumerate(entities):
        if entity['entity'].startswith('B-ORG'):
            org_name = entity['word']
            j = i + 1
            while j < len(entities) and entities[j]['entity'].startswith('I-ORG'):
                org_name += '' + entities[j]['word'][2:]
                j += 1
            institutions.add(org_name)

    author_affiliation = list(institutions)
    return author_affiliation


def get_affiliation_by_spacy(text):
    """
    使用 spacy 模型获取作者单位
    """
    # 加载预训练模型
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    institutions = set()
    # 提取组织实体
    for ent in doc.ents:
        if ent.label_ == "ORG":
            institutions.add(ent.text)

    author_affiliation = list(institutions)

    return author_affiliation


def get_affiliation_by_openai(text):
    """
    使用 OpenAI API 模型获取作者单位
    """
    prompt = 'Extract the organization names from the given text: ' + text

    # 调用 GPT-3.5 的接口
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very powerful named entity recognition model."},
            {"role": "user", "content": prompt}
        ],
    )

    output = response.choices[0].message.content.strip()
    institutions = [o.strip() for o in output.split("\n")]

    author_affiliation = list(set(institutions))

    return author_affiliation


def get_text_by_pdfplumber(pdf_url, methodType="openai"):
    """
    使用 pdfplumber 提取 PDF 文本并获取作者单位
    """
    # 从 URL 获取 PDF 文件内容
    response = requests.get(pdf_url)
    pdf_content = BytesIO(response.content)
    # 使用 pdfplumber 提取 PDF 文本
    with pdfplumber.open(pdf_content) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # 根据方法类型选择实体识别方法
        if methodType == 'openai':
            author_affiliation = get_affiliation_by_openai(text)

        if methodType == 'spacy_model':
            author_affiliation = get_affiliation_by_spacy(text)

        if methodType == 'bert_model':
            author_affiliation = get_affiliation_by_bert(text)

    return author_affiliation


if __name__=="__main__":

    pdf_url = 'https://arxiv.org/pdf/2304.10864.pdf'

    methodType = "bert_model"

    author_affiliation = get_text_by_pdfplumber(pdf_url, methodType)

    print('Author affiliation are: ', author_affiliation)
