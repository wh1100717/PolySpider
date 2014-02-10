[PolySpider] - New Android Crawler
==========
Python(v2.7) and Scrapy(v0.20.2) are used in this project, which is mainly designed for Android app synchronizing and categorizing by focusing on grabing data from Android Markets.

## Requirements
*	[Python] v2.7+
*	[Scrapy] v0.20+
*	[redis-py] v2.9+
*	[Supervisor] v3.0+
*	Dependencies are listed in [Installation]
*	ak & sk & bucket name of [BaiYun] or [Upyun] for files upload
*	Tested in Windows(both 32&64bit) and CentOS 6.4(64bit)

## Contribution Guides
1.	[Getting Involved]
2.	[Installation]
3.	[TODO List]
4.	[Core Functionalities]
5.	[Tips]

## Branch Descirption
* master branch

    >the latest stable version, which can be currently used in Poly Project. NEVER EVER straightly commit codes in MASTER branch.
* develop branch

    >the developing unstable version. team contributors should take code imporvement in this branch. If the project in develop branch comes to a stable level and meets the product requirement. The MASTER branch will merge the pull request from develop branch and release a stable branch version.
* stable branch

    >we use `numbers` like `0.1`, `0.3`, `1.0` as a stable release from this project.

* gh-pages branch

    >static resources and website page

## Usage
###Run Single Spider
1.	Step into `PolySpider/src/` directory
2.	Use `scrapy list` command to find spiders this project has provided
3.	Use `scrapy crawl spidername` command to start the crawler, which will crawl the target app market and then record the  crawled app information into sqlite database, download the apk file and parse it to get the info_list including pakage name, app name etc. If needed, it will upload the apk file to Cloud Storage like BaiduYun and UpYun.
4.	Since the app info is stored in sqlite database, you can use `python check_sql_data.py` command to check out what info the database has for convenience or just use some SqliteBrowser tools.

###Run supervisor
Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.

1.  All configuration setting of Supervisor is included in `PolySpider/src/supervisor.conf`
2.  Step into `PolySpider/src/` directory
3.  User `supervisord -c supervisor.conf` to start supervisor process and all python processes managed by Supervisor will start automatically. Moreover, Supervisor will monitor the process and restart them if the processes are interrupted or quit unexpectedly。
4.  Admin can watch the Supervisor status in browser with the address `localhost:9001` by default and there are some oprations could be taken on the python processes like `refresh`, `stop`, `restart` and so on.
5.  Directory named `PolySpider/src/tmp/` contains log files of Supervisor itself and other processes. Feel free to check it out!

## Supported Android Markets
*	[AppStar]
*	[AppChina]
*	[BaiduApp]
*	[Hiapk安卓市场]
*	[XiaomiApp]
*	[GooglePlay]


[AppStar]: http://www.appstar.com.cn/
[AppChina]: http://www.appchina.com/
[BaiduApp]: http://as.baidu.com/
[Hiapk安卓市场]: http://apk.hiapk.com/
[XiaomiApp]: http://app.xiaomi.com/
[GooglePlay]: https://play.google.com/store

[Python]: http://www.python.org/
[Scrapy]: http://www.scrapy.org/
[redis-py]: https://github.com/andymccurdy/redis-py
[Supervisor]: https://pypi.python.org/pypi/supervisor

[BaiYun]: http://developer.baidu.com
[Upyun]: https://www.upyun.com
[Getting Involved]: http://wh1100717.github.io/PolyTechDocs/docs/invovled/
[Installation]: http://wh1100717.github.io/PolyTechDocs/python/scrapy/installation/
[TODO List]: https://github.com/wh1100717/PolySpider/blob/master/docs/TODO_LIST.md
[Core Functionalities]: https://github.com/wh1100717/PolySpider/blob/master/docs/pipelineinfo.md
[Tips]: https://github.com/wh1100717/PolySpider/blob/master/docs/TIPS.md
[PolySpider]: https://github.com/wh1100717/PolySpider

