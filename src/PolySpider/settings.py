#!/usr/bin/env python
# -*- coding: utf-8 -*-  

BOT_NAME = 'PolySpider'

LOG_LEVEL='DEBUG'

SPIDER_MODULES = ['PolySpider.spiders']
NEWSPIDER_MODULE = 'PolySpider.spiders'

ITEM_PIPELINES = {
    'PolySpider.pipelines.PolySpiderPipeline' : 1,
    'PolySpider.pipelines.CategorizingPipeline': 100,
    'PolySpider.pipelines.CheckAppPipeline': 101,
    'PolySpider.pipelines.CheckAppDetailsPipeline': 102,
    'PolySpider.pipelines.UpdateCategoryPipeline': 103,
    'PolySpider.pipelines.StatusRecordPipeline': 104
}

#--------------------avoid banning:2 seconds once time--------------
DOWNLOAD_DELAY = 3
COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = True
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'PolySpider.util.RadomUseragentUtil.RotateUserAgentMiddleware' :400,
        #'PolySpider.utilTorUtil.ProxyMiddleware': 410,
    }
