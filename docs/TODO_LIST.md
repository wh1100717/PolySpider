## ApkUtil
*	利用aapt分析apk并获取pakage_name、version、icon等资源。
*	aapt只有32的，所以如果在64位服务器上运行需要增加一些32位依赖库
*	重新整理ApkUtil模块，添加注释和方法描述

## Spider
[AppStoreList]中详细分析了目前国内android应用商店的具体情况、特点和访问方式。通过其逐步添加针对性的spider。

*   [应用宝]：TODO
*   [拇指玩]：TODO
*   [机锋市场]：TODO
*   [360手机助手]: TODO

## Dynamic Content Grabbing
Scrapy只能实现静态页面的抓取，无法模拟浏览器，自动加载和执行js文件，导致动态请求内容无法获取。为了实现爬虫对于动态请求的抓取，需要模拟浏览器行为来实现爬虫对于多种类型网页的抓取工作。
*	[Selenium]
*	[ScrapyJS]
*	[Python Webkit]

## DB Problems
*	目前使用的是sqlite3，需要解决database locked问题
*	除了默认配置的sqlite3以外，打算添加mysql和mongodb作为备选可用数据库支持

## Categorizing
*	目前采用的91助手的分类策略，需要更改为google play的分类策略
*	增加前台用户直接更改某个应用的分类功能
*	增加分类查询、修改等各种接口

## Log System
*	日志系统包括spider的活动状态
*	日志系统包括数据库的操作记录
*	实现前端页面实时显示日志内容

## Ban&Proxy Strategy
* 	通过改变cookie
* 	通过middleware，不停的变user-aget
* 	更改访问时间等方法

## PEP8
项目需要统一代码格式和规范，而实际上PEP8提供了Python的代码规范格式说明和相应的规范检查工具。

*	阅读[PEP8--Style Guide for Python Code]，了解python编码规范，逐步养成符合PEP8编码规范的Python代码编写习惯
*	学习使用[pep8 - Python style guide checker]，利用pep8最代码做规范性检查
*	查找或者撰写中文PEP8代码规范文档，方便查询和阅读,为后续员工提供文档，形成规范

## Tornado
最终spider是作为任务常驻服务器，[Tornado]作为非阻塞式Python服务器，提供高并发等服务支持，需要去了解、搭建和配置Tornado，以及需要了解[非阻塞式编程方式]。另外可以了解[web.py]，其为轻量级python web框架，可能会用得着。

## API
设计、完善并规范API接口，实现其它系统的低耦合衔接。

##研究和学习的内容

###items.py
*	field（）升序降序
*	itemloader（）

###middleware
*	downloader middleware
*	CookiesMiddleware
*	defaultHeadersMiddleware
*	DownloadTimeoutMiddleware
*	HttpAuthMiddleware
*	HttpCacheMiddleware
*	HttpCompressionMiddleware
*	ChunkedTransferMiddleware
*	HttpProxyMiddleware
*	RedirectMiddleware
*	MetaRefreshMiddleware
*	RetryMiddleware
*	RobotsTxtMiddleware
*	DepthMiddleware
*	HttpErrorMiddleware
*	OffsiteMiddleware
*	RefererMiddleware
*	UrlLengthMiddleware

###__init __.py
*	了解及利用，完成相应的初始化

###from ... import ...
*	规范用法

###settings.py
*	了解settings.py，学习其他设置参数

###pipy及接口定义方式
*	了解上传pipy方法，尝试将polyspider做成一个API

[aapt]:https://code.google.com/p/android-apktool/
[Selenium]:http://www.seleniumhq.org/
[ScrapyJS]:https://github.com/scrapinghub/scrapyjs
[Python Webkit]: http://www.gnu.org/software/pythonwebkit/

[非阻塞式编程方式]:http://cnodejs.org/topic/4f50dd9798766f5a610b808a
[Tornado]:http://www.tornadoweb.org/en/stable/
[AppStoreList]:https://github.com/wh1100717/PolySpider/blob/master/APP_STORE_LIST.md
[web.py]:http://webpy.org/

[小米商店]:http://app.xiaomi.com/
[天翼空间]:http://www.189store.com/soft.html
[移动应用商店]:http://mm.10086.cn/
[沃商店]:http://store.wo.com.cn/
[应用宝]:http://android.myapp.com/
[91助手]:http://apk.91.com/
[百度应用]:http://as.baidu.com/
[机锋市场]:http://apk.gfan.com/
[360手机助手]:http://zhushou.360.cn/
[智汇云应用市场]:http://app.vmall.com/
[木蚂蚁应用市场]:http://www.mumayi.com/
[安卓市场]:http://apk.hiapk.com/
[拇指玩]:http://www.muzhiwan.com/
[Google Paly China]:https://play.google.com/store

[PEP8--Style Guide for Python Code]:http://www.python.org/dev/peps/pep-0008/
[pep8 - Python style guide checker]:https://pypi.python.org/pypi/pep8
