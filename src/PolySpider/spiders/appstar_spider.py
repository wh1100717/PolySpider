#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from PolySpider.items import AppItem
from PolySpider.config import Config
from PolySpider.util import CommonUtil
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem

class AppStarSpider(BaseSpider):
    '''
    ##AppStar: 应用之星
    *   网址http://www.appstar.com.cn
    *   因为其详细页格式为www.appstar.com.cn/ace/store/*.htm，其中*是从30到30000左右的数字，所以直接构造请求进行抓取即可
    '''
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

    def parse_app(self, response):	
        '''
        request的Callback处理函数，对于页面中能抓到的数据，利用xpath筛选内容
        xpath教程：http://www.w3school.com.cn/xpath/
        '''
        sel = Selector(response)
        item = AppItem()
        app_star=SpiderConfig.app_star
       
        
        print "Grabing Start：%s" % response.url
        for key in app_star:
            value = sel.xpath(app_star[key]).extract() if app_star[key]!='' else ''
            if key=='category':
                item[key] = value[1].strip() if len(value) !=0 else ''
            elif key=='android_version':
                item[key] = value[4].strip() if len(value) !=0 else ''
            else:
                item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
        item['app_name'] = CommonUtil.dropBrackets(item['app_name'])
        item['cover'] = "http://www.appstar.com.cn"+item['cover']
        item['version'] = CommonUtil.normalizeVersion(item['version'][4:-1])
        item['rating_point']=item['rating_point'][1:-2]
        item['rating_count']=item['rating_count'][:-3]
        item['category']=item['category'][5:]
        item['android_version'] = item['android_version'] [12:-1]
        item['download_times'] = item['download_times'] [5:-1]
        item['author']=item['author'][3:]
        item['last_update'] = item['last_update'][6:]
        item['apk_size']=item['apk_size'][5:]
        item['imgs_url']=' '.join(item['imgs_url'])
        item['platform'] = "appstar"
        print "Grabing finish, step into information pipline"
        return item
#        try:
#            sel = Selector(response)
#            item= AppItem()
#            print "Grabing Start：%s" %response.url
#            print len(sel.xpath("//*[@id='appDetail']/li[1]/a/@href").extract())
#            if len(sel.xpath("//*[@id='appDetail']/li[1]/a/@href").extract())==0 :
#                item['app_name']="" 
#                return item
#            else:
#                item['apk_url'] = "http://www.appstar.com.cn" + sel.xpath("//*[@id='appDetail']/li[1]/a/@href").extract()[0]
#                item['app_name'] = CommonUtil.dropBrackets(sel.xpath('//*[@id="appName"]/text()').extract()[0])
#                item['cover'] = "http://www.appstar.com.cn"+sel.xpath('//*[@id="appImg"]/@src').extract()[0]
#                item['version'] = CommonUtil.normalizeVersion(sel.xpath('//*[@id="appVersion"]/text()').extract()[0][4:-1])
#                item['rating_point'] = sel.xpath('//*[@id="appDetail"]/li[1]/span/text()').extract()[0][1:-2]
#                item['rating_count'] = sel.xpath('//*[@id="appDetail"]/li[2]/span[1]/text()').extract()[0][:-3]
#                item['category'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()').extract()[1][6:]
#                item['android_version'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()').extract()[4][12:-1]
#                item['download_times'] = CommonUtil.download_time_normalize(sel.xpath('//*[@id="appDetail"]/li[2]/text()[2]').extract()[0][5:-1])
#                author=sel.xpath('//*[@id="appDetail"]/li[2]/text()[3]').extract()
#                if len(author)==0:
#                    author = ''
#                else:
#                    author = author[0][3:]
#                item['author'] = author
#                item['last_update'] = sel.xpath('//*[@id="appDetail"]/li[2]/span[2]/text()').extract()[0][6:]
#                description = sel.xpath('//*[@id="appDes"]/p/text()').extract()
#                item['description'] = "" if description == [] else description[0].strip()
#                item['apk_size'] = sel.xpath('//*[@id="appDetail"]/li[1]/text()[3]').extract()[0][5:]
#
#                #获取图片地址，通过空格来分割多张图片
#                imgs =  sel.xpath('//li/img/@src').extract()
#                imgs_url = ""
#                for i in range(2,len(imgs)): imgs_url += "http://www.appstar.com.cn"+imgs[i] + " "
#                item['imgs_url'] = imgs_url.strip()
#                item['platform'] = "appstar"
#                print "Grabing finish, step into information pipline"
#                return item
#        except HTTPError:
#            item['app_name']=""
#            return item