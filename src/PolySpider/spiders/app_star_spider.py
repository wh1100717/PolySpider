#!/usr/bin/env python
#coding:gbk

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from PolySpider.items import AppItem
from PolySpider import Config

class AppStarSpider(BaseSpider):
	name = "app_star"
	allowed_domains = ["appstar.com.cn"]
	start_urls = [
                "http://appstar.com.cn/"
	]
        
        def parse(self,response):
            '''
            其应用详细页的格式为 http://www.appstar.com.cn/ace/store/n.htm
            n从30开始，总共大概有3W多个。
            所以利用循环分别构造带有相应url的请求，并利用yield返回给Scrapy进行内容抓取，response利用parse_app来纪念性处理和解析
            '''
            for i in range(30,30 + Config.APPSTAR_MAX_APPS):
                req = Request(url="http://www.appstar.com.cn/ace/store/"+str(i)+'.htm',callback = self.parse_app)
                yield req
        
        '''
        request的Callback处理函数，对于页面中能抓到的数据，利用xpath筛选内容
        xpath教程：http://www.w3school.com.cn/xpath/
	'''
        def parse_app(self, response):	
            sel = Selector(response)
            item= AppItem()
            item['apk_url'] = "http://www.appstar.com.cn" + sel.xpath("//*[@id='appDetail']/li[1]/a/@href").extract()[0]
            item['app_name'] = sel.xpath('//*[@id="appName"]/text()').extract()[0]
            item['cover'] = sel.xpath('//*[@id="appImg"]/@src').extract()[0]
            item['version'] = sel.xpath('//*[@id="appVersion"]/text()').extract()[0][4:-1]
            item['rating_star'] = sel.xpath('//*[@id="appDetail"]/li[1]/span/text()').extract()[0][1:-2]
            item['rating_count'] = sel.xpath('//*[@id="appDetail"]/li[2]/span[1]/text()').extract()[0][:-3]
            item['category'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()').extract()[1][6:]
            item['android_version'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()').extract()[4][5:]
            item['download_times'] = sel.xpath('//*[@id="appDetail"]/li[2]/text()').extract()[1][5:-1]
            item['author'] = sel.xpath('//*[@id="appDetail"]/li[2]/text()').extract()[2][3:]
            item['last_update'] = sel.xpath('//*[@id="appDetail"]/li[2]/span[2]/text()').extract()[0][6:]
            description = sel.xpath('//*[@id="appDes"]/p/text()').extract()
            item['description'] = "" if description == [] else description[0]
            item['apksize'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()[3]').extract()[0][5:]
            
            #获取图片地址，通过空格来分割多张图片
            imgs =  sel.xpath('//li/img/@src').extract()
            imgs_url = ""
            for i in range(2,len(imgs)): imgs_url += imgs[i] + " "
            item['imgs_url'] = imgs_url.strip()
            return item