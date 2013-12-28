## ApkParse
目前利用[aapt]对apk进行解压缩，提取出aapt构建的yml等文件获取相应的icon、pakage_name、version等内容。但是aapt会将apk文件整体解压，效率较慢。如果仅仅是获取部分apk信息，则没必要使用aapt来对apk进行整体解压缩,ApkParse模块需要研究并实现对于apk部分内容的分析。

apk反编译过程：

*	`unzip targetFile.apk`
*	`$ java -jar AXMLPrinter2.jar AndroidManifest.xml AndroidManifest2.xml`
*	这样就可以获取到可读的AndroidManifest.xml文件
*	但是在AndroidManifest.xml中有些信息是类似于`@7F080000`这样的
*	如果要获取实际信息则需要反编译classes.dex
*	`java -jar ddx1.11.jar -o -D -r -d src classes.dex`
*	在src/com/target/目录下面执行`$ grep -i 7F080000 *`可以获得该数值所代表的真正含义
*	根据具体的数值去获取相应的资源

在实际操作过程中发现，利用ddx解压classes.dex的时间占大部分，而如果为了获取AndroidManifest.xml中类似于`@7F080000`这样的字符串所代表的信息必须要家压缩classes.dex，而且获取所有信息需要做额外非常多的编码工作，又没有效率上的提升，所以还是建议使用aapt作为android的分析和开发工具。为了增加解压缩速度，aapt需要增加`-s`参数(Do not decode sources.)。


## Selenium
Scrapy只能实现静态页面的抓取，无法模拟浏览器，自动加载和执行js文件，导致动态请求内容无法获取。为了实现爬虫对于动态请求的抓取，需要利用[Selenium]来模拟浏览器行为，Scarpy集合Selenium来实现爬虫对于多种类型网页的抓取工作。
## Spider
[AppStoreList]中详细分析了目前国内android应用商店的具体情况、特点和访问方式。通过其逐步添加针对性的spider。

*   [小米商店]：TODO
*   [应用宝]：TODO
*   [百度应用]：TODO
*   [安卓市场]：TODO
*   [拇指玩]：TODO

## Sqlite
逐步添加sqlite的查询工作，撰写python脚本，根据不同的请求进行sqlite的查询。
## Tornado
最终spider是作为任务常驻服务器，[Tornado]作为非阻塞式Python服务器，提供高并发等服务支持，需要去了解、搭建和配置Tornado，以及需要了解[非阻塞式编程方式]。另外可以了解[web.py]，其为轻量级python web框架，可能会用得着。
## Categorizing
目前采取91助手的分类策略，建立字典对其它应用市场的分类与其做对应关系(可以是1对多的关系)。这样抓取的任何一个应用都能与系统中的分类做对应。

    我在想，如果有些分类比较笼统话，是否可以做出一定的策略，而不是将该分类之间确定为某一个我们的分类
    比如App_star中的办公分类，实际上是一个笼统概念，无法直接与我们的分类进行对应
    比如将其分类设置为需要额外一些工作来进行确认的分类
    比如一个应用如果是办公分类，首先查看其是否已经grab到数据库中，如果数据库中对这个应用已经有记录，那么直接那个记录来分类
    如果没有记录，则指定某个默认分类来记录，等待别的应用商店上传该应用，来分类，或者该应用进行人工分类的操作等等
    再比如，可以对应用分类进行命中率划分，也就是说10个应用商店，其中有6个把其划分到“效率”，那么效率的命中率就是60%，我们默认采用的是命中率最高的分类方式等等。

## Architecture
目前使用的Scrapy的默认结构，实际上Scrapy对该结构做了一些默认配置，从而能够方便的进行爬虫开发，而又不用担心配置问题。但是随着spider数量的增加，组织结构就会变得越来越臃肿和困难，一定会增加后期开发的难度和扩展性。所以重构项目组织结构，更改配置，提高代码的重用性和清晰度也在计划中。
## Download && Upload

*   下载进度条          Done
*   UpYun上传进度条     Done
*   BaidYun上传进度条   TODO


[aapt]:https://code.google.com/p/android-apktool/
[Selenium]:http://www.seleniumhq.org/
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
[Google Play]:https://play.google.com/store
