[PolySpider] - New Android Crawler
==========
Python(v2.7) and Scrapy(v0.20.2) are used in this project, which mainly focus on grabing data from Android Markets, meanwhile, it is designed for android app synchronizing and categorizing.

## Requirements
*	[Python] v2.7+
*	[Scrapy] v0.20+
*	ak & sk & bucket name of [BaiYun] or [Upyun] for files upload
*	Only test in Windows(both 32&64bit), but it should work much better in Linux or Unix I think...

## Contribution Guides
1.	[Getting Involved]
2.	[Installation]
3.	Core Functionalities
4.	Tips

## Usage
1.	step into `PolySpider/src/` directory
2.	`scrapy list` to find the spider this project has provided
3.	use `scrapy crawl spidername` to start the crawler, which will crawl the target app market and then record the  crawled app information into sqlite database, download the apk file and parse it to get the info_list including pakage name, app name .etc. If needed, it will upload the apk file into Cloud Storage like BaiduYun and UpYun.
4.	since the app info is stored in sqlite database, u can use `python check_sql_data.py` to check out what info the database for convenience.
5.	More usage command would be added soon...

## Supported Android Markets
*	[AppStar]
*	More android market spider would be released soon




[AppStar]:http://www.appstar.com.cn/
[Python]:http://www.python.org/
[Scrapy]:http://www.scrapy.org/
[BaiYun]:http://developer.baidu.com
[Upyun]:https://www.upyun.com
[Getting Involved]:http://wh1100717.github.io/PolyTechDocs/docs/invovled/
[Installation]: http://wh1100717.github.io/PolyTechDocs/python/scrapy/installation/
[PolySpider]: https://github.com/wh1100717/PolySpider
