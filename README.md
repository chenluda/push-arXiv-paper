# pushArXivPaper
## 每天定点向微信推送 arXiv 最新文章

作为科研人，每天早起的第一件事，

就是打开 arXiv 查找自己 follow 的领域有没有最新的文章。

现在我想把这件事自动化：

类似部署自动打卡函数，在阿里云函数计算 FC 中设置一个带有定时触发器的云函数，

再将每天定点向微信推送 arXiv 最新文章的脚本程序部署上去，

实现：

根据关键词搜索在 arXiv 发布的文章；
判断文章的发布日期是否是前一天（或指定日期），如果是，则保留；
使用 Server 酱将前一天文章的标题、网址、摘要推送至微信。

效果展示：

![image](https://github.com/chenluda/pushArXivPaper/assets/45784833/40974b09-c120-4eaa-a8c4-90908ce18f92)

这里我为了展示效果，将条件“前一天发布”改为了特定条件“2023 年 4 月 12 日发布”。

![image](https://github.com/chenluda/pushArXivPaper/assets/45784833/dfd21de4-8ae2-48b4-ac12-198fe19b4c85)

---

使用 gpt3.5 识别论文的作者单位，如果不需要的话，可以注释掉相关代码。

其中，handler 函数中的 SERVERCHAN_API_KEY、search_term 、max_results 是根据需求修改的变量。

* SERVERCHAN_API_KEY：自己 Serve 酱的 API（下方会解释）。
* search_term：搜索论文的关键词，如果使用双引号将词包裹起来，表明论文中必须出现这个词，例如，'Masked Image Model' 和 '"Masked Image Model"' 搜索结果不同，具体请查看 arxiv 的文献检索说明。
* max_results：检索论文的最大数量。
如果想直接本地运行，则可以将 def handler(event, context): 改为 if __name__ == '__main__': 。
