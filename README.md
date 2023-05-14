# pushArXivPaper
## 每天定点向微信推送 arXiv 最新文章

作为科研人，每天早起的第一件事，

就是打开 arXiv 查找自己 follow 的领域有没有最新的文章。

现在我想把这件事自动化：

类似部署自动打卡函数，在阿里云函数计算 FC 中设置一个带有定时触发器的云函数，

再将每天定点向微信推送 arXiv 最新文章的脚本程序部署上去，

实现：

* 根据关键词搜索在 arXiv 发布的文章；
* 判断文章的发布日期是否是前一天（或指定日期），如果是，则保留；
* 使用 Server 酱将前一天文章的标题、网址、摘要推送至微信。

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
---

### 1. Server 酱

我们需要使用到Server 酱，这是一款从服务器、路由器等设备上推消息到手机的工具。我们需要使用她实现向微信推送消息的功能。

* 打开官网网址：[https://sct.ftqq.com/](https://link.zhihu.com/?target=https%3A//sct.ftqq.com/)；
* 微信扫码登陆后，进入 Key&API 模块；
* 将 SendKey 复制替换代码中的 Your-Server-API。
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/c968d2ca-e36c-4769-87c8-02f1df4cf91b)

### 2. 阿里云函数计算 FC

函数计算（Function Compute）是一个事件驱动的全托管 Serverless 计算服务，无需管理服务器等基础设施，只需编写代码并上传，函数计算会准备好计算资源，并以弹性、可靠的方式运行代码。

* 打开官网网址：[国内唯一入选Forrester领导者象限](https://link.zhihu.com/?target=https%3A//www.aliyun.com/product/fc%3Fspm%3D5176.28055625.J_3207526240.99.4d9c154a5PXJtz%26scm%3D20140722.S_function%40%40product%40%4090871._.ID_function%40%40product%40%4090871-RL_%25E5%2587%25BD%25E6%2595%25B0%25E8%25AE%25A1%25E7%25AE%2597-LOC_bar-OR_ser-V_2-P0_0)，登陆后，进入管理控制台；
* 进入服务及函数模块，点击创建服务按钮；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/7f93da1e-28be-4631-86cd-3fa366ae9a74)

* 将弹窗中的名称和描述填完后，点击左下角确定按钮；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/67c8fcf8-93d7-4bc4-8239-0f5139099f82)

* 进入函数管理模块，点击创建函数按钮；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/ed90c8ea-ba77-4797-9f55-9c5940851527)

* 填写函数名称；
* 将上面给出的脚本代码保存为 [index.py](https://link.zhihu.com/?target=http%3A//index.py/) 放入一个名为 arxiv\_push\_code 的空文件夹中；
* 压缩该文件夹，将压缩包拖至代码包处；
* 点击页面下方创建按钮；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/b2a41478-1f45-4159-aca7-4e864edc0d3a)

* 将 arxiv\_push\_code 文件夹中的 [index.py](https://link.zhihu.com/?target=http%3A//index.py/) 拖至上级文件夹 CODE 处；
* 将 arxiv\_push\_code 文件夹删除；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/876a1deb-c04e-481d-a856-5776f29ca4de)

* 进入触发器管理模块，点击创建触发器按钮；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/bf5e9ceb-e10f-438c-b6de-bda5e07298de)

* 在弹窗中填写相关内容，其中“指定时间”就是在设置每天几点向微信推送文章；
* 填写完后点击左下方确定按钮，完成触发器创建；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/95ec33a9-0b93-4ae5-a6a4-54c24a765514)

* 回到函数代码页面，点击部署代码按钮，出现部署成功提示后，表示部署成功；
![image](https://github.com/chenluda/push-arXiv-paper/assets/45784833/d717cc18-2ccf-4c1d-b21c-0bd71f4fc619)

* 点击测试函数，可以直接运行。
