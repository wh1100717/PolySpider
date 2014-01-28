#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem
from PolySpider.util import CommonUtil

class GooglePlaySpider(CrawlSpider):
    '''
    ##GooglePlay: Google 市场市场
    *   网址https://play.google.com/
    *   利用Rule规则进行抓取
    '''
    name = "googleplay"
    allowed_domains = ["google.com"]
    start_urls = [
        "https://play.google.com/store/"        
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('play.google.com/store/apps/category/', )),follow=True),
        Rule(SgmlLinkExtractor(allow=('play.google.com/store/apps/details\?id=', )),callback='parse_app',follow=True)
    ]
    def parse_app(self, response):
        
        sel = Selector(response)
        item = AppItem()
        google_play = SpiderConfig.google_play
        print "Grabing Start：%s" % response.url
        # 根据SpiderConfig中的xpath配置进行抓取数据
        for key in google_play:
            value = sel.xpath(google_play[key]).extract() if google_play[key]!='' else ''
            item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
        item['imgs_url'] = " ".join(item['imgs_url'])    
        item['cover'] = item['cover'][0]
        item['download_times']=item['download_times'].replace(',','')[:item['download_times'].find('-')]
        item['rating_count']= item['rating_count'].replace(',','')
        item['platform'] = "googleplay"
        print "Grabing finish, step into information pipline"
        return item
      
