#!/usr/bin/env python
#coding:gbk

BOT_NAME = 'PolySpider'

SPIDER_MODULES = ['PolySpider.spiders']
NEWSPIDER_MODULE = 'PolySpider.spiders'

ITEM_PIPELINES = {
    'PolySpider.pipelines.PolySpiderPipeline' : 100,
    'PolySpider.pipelines.AppStarSpiderPipeline': 200
}

#--------------------avoid banning:2 seconds once time--------------
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

#App Star Constant
APPSTAR_MAX_APPS = 30000

#BaiduYun AK && SK
BAIDU_AK = 'NEED TO BE FILLED'
BAIDU_SK = 'NEED TO BE FILLED'
BAIDU_BUCKET = 'NEED TO BE FILLED'