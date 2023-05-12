'''
Description: 每天定点向微信推送 arXiv 最新文章
Version: 1.0
Author: Glenn
Email: chenluda01@outlook.com
Date: 2023-04-19 08:35:13
FilePath: index.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''

import datetime
import os
import time
from io import BytesIO

import openai
import pdfplumber
import requests


def get_author_affiliation(pdf_url):
    """
    从 PDF 文件中提取作者单位信息
    """
    response = requests.get(pdf_url)
    pdf_content = BytesIO(response.content)
    author_affiliation = []

    with pdfplumber.open(pdf_content) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # 设置提示词
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


def get_yesterday():
    """
    获取前一天的日期
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def search_arxiv_papers(search_term, yester_date, max_results=10):
    """
    在 arxiv 按照关键词查找前一天的论文
    """
    papers = []

    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'search_query=all:{search_term}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    response = requests.get(base_url + search_query)
    
    if response.status_code != 200:
        print("请求失败，请检查你的查询参数。")
        return

    feed = response.text
    entries = feed.split('<entry>')[1:]
    
    if not entries:
        print("没有找到与搜索词匹配的论文。")
        return
    
    for entry in entries:
        # 获取标题、摘要、链接、首次发布日期
        title = entry.split('<title>')[1].split('</title>')[0].strip()
        summary = entry.split('<summary>')[1].split('</summary>')[0].strip()
        url = entry.split('<id>')[1].split('</id>')[0].strip()
        pub_date = entry.split('<published>')[1].split('</published>')[0]
        pub_date = datetime.datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        # 获取 PDF 链接
        pdf_url = entry.split('<link href="')[1].split('" rel="alternate')[0].strip()
        pdf_url = pdf_url.replace("abs", "pdf")

        # 获取作者单位
        author_affiliation = get_author_affiliation(pdf_url)

        if pub_date == yester_date:
            papers.append({
                'title': title,
                'url': url,
                'pub_date': pub_date,
                'summary': summary,
                'author_affiliation': author_affiliation
            })
        
    return papers

def send_wechat_message(title, content, SERVERCHAN_API_KEY):
    """
    使用 Serve 酱向微信推送论文信息
    """
    url = f'https://sctapi.ftqq.com/{SERVERCHAN_API_KEY}.send'
    params = {
        'title': title,
        'desp': content,
    }
    requests.post(url, params=params)


# def handler(event, context):
if __name__ == '__main__':
    # 设置 OPENAI 的 API_KEY
    os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # 修改为自己 Serve 酱 API
    SERVERCHAN_API_KEY = 'SCT206421TeQFPxkyqpZQFegFELJaKCW6d'
    # 关键词
    search_term = '"masked image model"'
    # 获取的最大论文数
    max_results = 10
    # 获取前一天的日期
    yester_date = get_yesterday()
    # 在 arxiv 按照关键词查找前一天的论文
    papers = search_arxiv_papers(search_term, yester_date, max_results)

    for paper in papers:
        title = paper['title']
        url = paper['url']
        pub_date = paper['pub_date']
        summary = paper['summary']

        msg_title = f'标题：{title}'
        msg_url = f'论文网址：{url}'
        msg_pub_date = f'首次发布时间：{pub_date}'
        msg_summary = f'摘要：{summary}'

        msg_content = f'{msg_title}\n\n{msg_url}\n\n{msg_pub_date}\n\n{msg_summary}'
        
        send_wechat_message(title, msg_content, SERVERCHAN_API_KEY)

        # 为避免触发微信推送服务的限制，等待一段时间后再发送下一篇论文的信息
        time.sleep(5)
