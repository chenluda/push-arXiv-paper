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
