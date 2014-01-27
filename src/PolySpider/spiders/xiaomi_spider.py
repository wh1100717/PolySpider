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
class XiaomiSpider(BaseSpider):
    '''
    ##Xiaomi: 小米商店
    *   网址http://app.xiaomi.com/
    *   小米商店的应用详细页格式为http://app.xiaomi.com/detail/*，所以很好抓，不需要用rule，直接循环构造请求即可
    '''
    name = "xiaomi"
    allowed_domains = ["xiaomi.com"]
    start_urls = [
        "http://app.xiaomi.com/"
    ]

    def parse(self,response):
        '''
        其应用详细页的格式为 http://app.xiaomi.com/detail/1127
        所以利用循环分别构造带有相应url的请求，并利用yield返回给Scrapy进行内容抓取，response利用parse_app来纪念性处理和解析
        '''
        for i in range(1,1 + Config.APPSTAR_MAX_APPS):
            req = Request(url="http://app.xiaomi.com/detail/"+str(i),callback = self.parse_app)
            yield req
    def parse_app(self, response):	
        sel = Selector(response)
        item= AppItem()
        xiaomi = SpiderConfig.xiaomi
        if sel.xpath(xiaomi['app_name']).extract() == []:
            raise DropItem(item)
        print "Grabing Start：%s" % response.url
        # 根据SpiderConfig中的xpath配置进行抓取数据
        for key in xiaomi:
            value = sel.xpath(xiaomi[key]).extract() if xiaomi[key]!='' else ''
            item[key] = value[0].strip().decode('utf8') if len(value) == 1 else ('' if len(value) == 0 else value)
        item['apk_url'] = "http://app.xiaomi.com"+item['apk_url']
        item['rating_point']=item['rating_point'][11:]
        item['description']=' '.join(item['description'])
        item['imgs_url']=' '.join(item['imgs_url'])
        item['platform'] = "xiaomi"
        print "Grabing finish, step into information pipline"
        return item
#        try:
#            print "Grabing Start：%s" %response.url
#            apk_url = sel.xpath('/html/body/div[2]/div[1]/div[3]/div[1]/a/@href').extract()
#            if len(apk_url)==0:
#                item['app_name']=''
#                return item
#            else:
#                item['apk_url'] = "http://app.xiaomi.com" +  apk_url[0]
#                item['app_name'] = CommonUtil.dropBrackets(sel.xpath('/html/body/div[2]/div[1]/div[2]/h1/text()').extract()[0])
#                item['cover'] = sel .xpath("/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/img/@src").extract()[0]
#                version=sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[2]/h4/text()').extract()
#                item['version'] = '' if len(version)==0 else CommonUtil.normalizeVersion(version[0])
#                item['rating_point'] = sel.xpath('/html/body/div[2]/div[1]/div[3]/div[1]/div[2]/@class').extract()[0][11:]
#                item['rating_count'] = '0'#小米商店没有评价数
#                item['category'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[1]/h4/text()').extract()[0]
#                item['android_version'] = '0'#小米商店没有支持的android版本信息
#                item['download_times'] = '0'#小米商店没有应用下载次数
#                item['author'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[6]/h4/text()').extract()[0]
#                item['last_update'] =  sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[3]/h4/text()').extract()[0]
#                descriptions = sel.xpath('/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/p/text()').extract()
#                alldescription=''
#                for description in descriptions:
#                    alldescription=alldescription+description
#                item['description'] = alldescription.strip()
#                item['apk_size'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[5]/h4/text()').extract()[0]
#                #获取图片地址，通过空格来分割多张图片
#                imgs =  sel.xpath('//*[@id="J_thumbnail_wrap"]/img/@src').extract()
#                imgs_url = ""
#                for img in imgs: imgs_url += img + " "
#                item['imgs_url'] = imgs_url.strip()
#                item['platform'] = "xiaomi"
#                print "Grabing finish, step into information pipline"
#                return item
#        except Exception:
#            item['app_name']=""
#            return item