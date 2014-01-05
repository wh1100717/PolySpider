[PolySpider] - New Android Crawler
==========
Python(v2.7) and Scrapy(v0.20.2) are used in this project, which is mainly designed for Android app synchronizing and categorizing by focusing on grabing data from Android Markets.

## Requirements
*	[Python] v2.7+
*	[Scrapy] v0.20+
*	[web.py] v0.37+
*	Dependencies are listed in [Installation]
*	ak & sk & bucket name of [BaiYun] or [Upyun] for files upload
*	Only test in Windows(both 32&64bit), but it should work much better in Linux or Unix I suppose...

## Contribution Guides
1.	[Getting Involved]
2.	[Installation]
3.	[TODO List]
4.	Core Functionalities
5.	Tips

## Usage
1.	step into `PolySpider/src/` directory
2.	use `scrapy list` command to find spiders this project has provided
3.	use `scrapy crawl spidername` command to start the crawler, which will crawl the target app market and then record the  crawled app information into sqlite database, download the apk file and parse it to get the info_list including pakage name, app name etc. If needed, it will upload the apk file to Cloud Storage like BaiduYun and UpYun.
4.	since the app info is stored in sqlite database, you can use `python check_sql_data.py` command to check out what info the database has for convenience or just use some SqliteBrowser tools.
5.	There is a frontend project based on HTML5 in the folder `PolySpider/src/web/` using web.py python web framework. It also integrate BootStrap3 as the frontend framework and some plugins like highcharts, highstock, datatables and so on. Only need to step into `PolySpider/src/web/` directory and use `python polySpider.py` command to set up a host server and browser the site with `localhost:8080` link address.
6.	More usage command would be added soon...

## Supported Android Markets
*	[AppStar]
*	[AppChina]
*	[BaiduApp]
*	[Hiapk安卓市场]
*	[XiaomiApp]
*	More Android market spiders would be released soon



[AppStar]: http://www.appstar.com.cn/
[AppChina]: http://www.appchina.com/
[BaiduApp]: http://as.baidu.com/
[Hiapk安卓市场]: http://apk.hiapk.com/
[XiaomiApp]: http://app.xiaomi.com/

[Python]: http://www.python.org/
[Scrapy]: http://www.scrapy.org/
[web.py]: http://webpy.org/
[BaiYun]: http://developer.baidu.com
[Upyun]: https://www.upyun.com
[Getting Involved]: http://wh1100717.github.io/PolyTechDocs/docs/invovled/
[Installation]: http://wh1100717.github.io/PolyTechDocs/python/scrapy/installation/
[TODO List]: https://github.com/wh1100717/PolySpider/blob/master/TODO_LIST.md
[PolySpider]: https://github.com/wh1100717/PolySpider
