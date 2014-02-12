## ApkUtil
[ApkTool]对apk进行解压缩，提取出aapt构建的yml等文件获取相应的icon、package_name、version等内容。但是ApkTool会将apk文件整体解压，效率较慢。如果仅仅是获取部分apk信息，则可以使用aapt直接读取apk中的一些基本信息,ApkUtil模块主要研究并实现对Apk的各种分析，其中用到了ApkTool实现apk的反编译和重新打包，aapt获取apk配置信息等内容。

Apk反编译过程：

*	`unzip targetFile.apk`
*	`$ java -jar AXMLPrinter2.jar AndroidManifest.xml AndroidManifest2.xml`
*	这样就可以获取到可读的AndroidManifest.xml文件
*	但是在AndroidManifest.xml中有些信息是类似于`@7F080000`这样的
*	如果要获取实际信息则需要反编译classes.dex
*	`java -jar ddx1.11.jar -o -D -r -d src classes.dex`
*	在src/com/target/目录下面执行`$ grep -i 7F080000 *`可以获得该数值所代表的真正含义
*	根据具体的数值去获取相应的资源

在实际操作过程中发现，利用ddx解压classes.dex的时间占大部分，而如果为了获取AndroidManifest.xml中类似于`@7F080000`这样的字符串所代表的信息必须要解压缩classes.dex，而且获取所有信息需要做额外非常多的编码工作，又没有效率上的提升，所以还是建议使用ApkTool作为android的反编译工具。

## Categorizing
*	目前采取91助手的分类策略，建立字典对其它应用市场的分类与其做对应关系(可以是1对多的关系)。这样抓取的任何一个应用都能与系统中的分类做对应。
*	我们对应用分类统计做了命中率系统，比如说10个商店有该应用，其中6个把其划分为“效率”，那么效率的命中率就是60%，我们默认采用命中率最高的作为对应的默认分类
*	计划增加人工修改分类的功能，目前的想法是将其命中次数更改为9999。

## Architecture
该项目中包含PolySpider和web两部分。分别为爬虫项目和前端展示项目。web项目主要包括静态文件和request响应和response内容生成。具体的业务逻辑和数据逻辑放在PolySpider项目中。

	Project Root
	├─.git
	└─src/
	    ├─scrapy.cfg		//scrapy项目配置文件
	    ├─app.db			//sqlite3数据库文件
	    ├─supervisor.conf		//Supervisor配置文件
	    ├─un_record_category.txt	//为识别的category记录文件
	    ├─PolySpider/
	    │  ├─config/  		//配置信息存放在这里
	    │  ├─spiders/ 		//爬虫模块
	    │  ├─sql/     		//涉及到特定数据库操作的方法
	    │  ├─tools/   		//爬虫需要的一些工具
	    │  ├─util/    		//一些公用方法
	    │  ├─items.py   		//model定义模块
	    │  ├─pipelines.py   	//抓取数据处理模块Core Module
	    │  └─settings.py		//scrapy配置模块
	    └─web/
	        ├─static/		//存放静态文件
	        ├─templates/		//存放模版文件
	        └─polySpider.py	//web.py的中心控制文件

## Download && Upload
*	实现apk下载到本机及进度条显示功能
*	实现百度云上传功能
*	重写又拍云api，实现上传及进度条查看上传进度功能
