#!/usr/bin/env python
#coding:gbk

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from PolySpider.items import AppItem
from PolySpider import settings

class AppStarSpider(BaseSpider):
	name = "app_star"
	allowed_domains = ["appstar.com.cn"]
	start_urls = [
                "http://appstar.com.cn/"
	]
        
        def parse(self,response):
            for i in range(30,30 + settings.APPSTAR_MAX_APPS):
                req = Request(url="http://www.appstar.com.cn/ace/store/"+str(i)+'.htm',callback = self.parse_app)
                yield req
                
	def parse_app(self, response):	
            sel = Selector(response)
            item= AppItem()
            item['apk_url'] = "http://www.appstar.com.cn" + sel.xpath("//*[@id='appDetail']/li[1]/a/@href").extract()[0]
            return item