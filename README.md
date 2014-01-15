[PolySpider] - New Android Crawler
==========
Python(v2.7) and Scrapy(v0.20.2) are used in this project, which is mainly designed for Android app synchronizing and categorizing by focusing on grabing data from Android Markets.

This project also contains a website project using web.py as the web framework, which is really easy-use, and bootstrap as fronten framework. Hightcharts, Highstock and Datatables are also included in this project. The website focus on showing data in different views and dimensions.

## Requirements
*	[Python] v2.7+
*	[Scrapy] v0.20+
*	[web.py] v0.37+
*	[Supervisor] v3.0+
*	Dependencies are listed in [Installation]
*	ak & sk & bucket name of [BaiYun] or [Upyun] for files upload
*	Only test in Windows(both 32&64bit), but it should work much better in Linux or Unix I suppose...

## Contribution Guides
1.	[Getting Involved]
2.	[Installation]
3.	[TODO List]
4.	[Core Functionalities]

## Usage
###Run Single Spider
1.	Step into `PolySpider/src/` directory
2.	Use `scrapy list` command to find spiders this project has provided
3.	Use `scrapy crawl spidername` command to start the crawler, which will crawl the target app market and then record the  crawled app information into sqlite database, download the apk file and parse it to get the info_list including pakage name, app name etc. If needed, it will upload the apk file to Cloud Storage like BaiduYun and UpYun.
4.	Since the app info is stored in sqlite database, you can use `python check_sql_data.py` command to check out what info the database has for convenience or just use some SqliteBrowser tools.

###Run web frontend
There is a frontend project based on HTML5 in the folder `PolySpider/src/web/` using web.py python web framework. It also integrate BootStrap3 as the frontend framework and some plugins like highcharts, highstock, datatables and so on.

1.  Step into `PolySpider/src/web/` directory
2.  Use `python polySpider.py` command to set up a host server.(you can also use `python polySpider.py portname`) to specify a particular port.
3.  Just browser this website with `localhost:portname` link address.

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


[AppStar]: http://www.appstar.com.cn/
[AppChina]: http://www.appchina.com/
[BaiduApp]: http://as.baidu.com/
[Hiapk安卓市场]: http://apk.hiapk.com/
[XiaomiApp]: http://app.xiaomi.com/

[Python]: http://www.python.org/
[Scrapy]: http://www.scrapy.org/
[web.py]: http://webpy.org/
[Supervisor]: https://pypi.python.org/pypi/supervisor

[BaiYun]: http://developer.baidu.com
[Upyun]: https://www.upyun.com
[Getting Involved]: http://wh1100717.github.io/PolyTechDocs/docs/invovled/
[Installation]: http://wh1100717.github.io/PolyTechDocs/python/scrapy/installation/
[TODO List]: https://github.com/wh1100717/PolySpider/blob/master/TODO_LIST.md
[Core Functionalities]: https://github.com/wh1100717/PolySpider/blob/master/pipelineinfo.md
[PolySpider]: https://github.com/wh1100717/PolySpider
