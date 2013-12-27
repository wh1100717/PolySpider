## ApkParse
目前利用[aapt]对apk进行解压缩，提取出aapt构建的yml等文件获取相应的icon、pakage_name、version等内容。但是aapt会将apk文件整体解压，效率较慢。如果仅仅是获取部分apk信息，则没必要使用aapt来对apk进行整体解压缩,ApkParse模块需要研究并实现对于apk部分内容的分析。
## Selenium
Scrapy只能实现静态页面的抓取，无法模拟浏览器，自动加载和执行js文件，导致动态请求内容无法获取。为了实现爬虫对于动态请求的抓取，需要利用[Selenium]来模拟浏览器行为，Scarpy集合Selenium来实现爬虫对于多种类型网页的抓取工作。
## Spider
[AppStoreList]中详细分析了目前国内android应用商店的具体情况、特点和访问方式。通过其逐步添加针对性的spider。
## Sqlite
逐步添加sqlite的查询工作，撰写python脚本，根据不同的请求进行sqlite的查询。
## Tornado
最终spider是作为任务常驻服务器，[Tornado]作为非阻塞式Python服务器，提供高并发等服务支持，需要去了解、搭建和配置Tornado，以及需要了解[非阻塞式编程方式]。另外可以了解[web.py]，其为轻量级python web框架，可能会用得着。
## Categorizing
目前仅仅是将应用的分类抓取并存放在sqlite的category字段上。但是实际上相同的应用可能不止一个分类，同一个应用在不同的应用商店分类可能不同，即使相同，分类名称也许也不相同。所以需要建立一整套的分类规范，通过分析抓取的分类名，将其归类到我们建立的分类系统中，使得从不同Android市场中抓取的应用可以轻松的划归到我们的分类系统里边。另外，需要讨论应用是否可以归属多个分类等方面的问题
## Architecture
目前使用的Scrapy的默认结构，实际上Scrapy对该结构做了一些默认配置，从而能够方便的进行爬虫开发，而又不用担心配置问题。但是随着spider数量的增加，组织结构就会变得越来越臃肿和困难，一定会增加后期开发的难度和扩展性。所以重构项目组织结构，更改配置，提高代码的重用性和清晰度也在计划中。
## Download
现在下载操作只是调用了urblib来对文件进行下载，但是不能监控下载的进度，需要完善下载流程，包括进度条，下载速度等内容。


[aapt]:https://code.google.com/p/android-apktool/
[Selenium]:http://www.seleniumhq.org/
[非阻塞式编程方式]:http://cnodejs.org/topic/4f50dd9798766f5a610b808a
[Tornado]:http://www.tornadoweb.org/en/stable/
[AppStoreList]:https://github.com/wh1100717/PolySpider/blob/master/APP_STORE_LIST.md
[web.py]:http://webpy.org/
