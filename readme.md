# personal weibo download
version : 1.0

从14年就在用新浪微博，在微博上记录了很多日常生活，相当于日记本，和它一起度过了三分之一的人生，承载了part of me。但是22年年初微博的随机捂嘴炸号行为敲醒了我。沉默和顺从只会助长嚣张气焰，铁链挂在每位女性脖子上。

***
**GirlsHelpGirls**
***

## usage
这个代码是课余时间写的，参考了一些网络上的代码，仅用于保存个人原创微博。

1.下载项目 git@github.com:JYueqi/personal_weibo_download.git

2.修改 config.py

* url,uid : 个人微博主页的网页，主要修改uid。**这里微博爬取是基于www.weibo.cn的，不适用于.com**
* cookies : 登录微博主页后，获取cookies，详细操作步骤参考：[手动获取cookies](https://blog.csdn.net/weixin_46089149/article/details/117694994)
* download_root : 微博图片保存路径
* weibo_data_path : 微博文本保存在csv文件中，csv文件的路径
* log_path : 日志存储路径

3.run main.py