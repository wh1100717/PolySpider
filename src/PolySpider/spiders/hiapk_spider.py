#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem

from PolySpider.util import CommonUtil

class AppStarSpider(CrawlSpider):
	name = "hiapk"
	allowed_domains = ["apk.hiapk.com"]
	start_urls = [
                "http://apk.hiapk.com"
	]
        rules = [
            Rule(SgmlLinkExtractor(allow=("apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )),callback='parse_app'),
            Rule(SgmlLinkExtractor(allow=("apk\.hiapk\.com", ),deny=("down\.apk\.hiapk\.com","apk\.hiapk\.com/Download\.aspx", )), follow = True),
        ]
	def parse_app(self, response):	
            sel = Selector(response)
            item = AppItem()
            print "抓取开始：%s" %response.url
            req=urllib2.Request("http://apk.hiapk.com" +   sel.xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href').extract()[0])
            req.add_header('referer', response.url)

            item['apk_url'] = urllib2.urlopen(req).url
            item['app_name'] = CommonUtil.dropBrackets(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()').extract()[0])
            item['cover'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src').extract()[0]
            item['version'] = CommonUtil.normalizeVersion(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()').extract()[0])
            item['category'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()').extract()[0]
            item['android_version'] =sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()').extract()[0]
            item['download_times'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()').extract()[0]
            author =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()
            if len(author)==0:
                author = ''
            else:
                author = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()[0]
            item['author'] = author
            item['last_update'] =   sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftPublishTime"]/text()').extract()[0]
            description=sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()').extract()
            if len(description)==0:
                description =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/p/text()').extract()[0]
            else:
                description =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()').extract()[0]
            item['description']=description.strip()
            item['apk_size'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSize"]/text()').extract()[0]
            rating_star = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/@class').extract()[0]
            if len(rating_star) < 21:
                item['rating_star'] = "0"
                item['rating_count'] = "0"
            else:
                item['rating_star'] = rating_star[21:-2] if len(rating_star) > 21 else "0"
                if "half" in item['rating_star']: item['rating_star'] = item['rating_star'][0] + ".5"
                item['rating_count'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()').extract()[0][:-3]
            #获取图片地址，通过空格来分割多张图片
            imgs =  sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href').extract()
            imgs_url = ""
            for img in imgs: imgs_url += img + " "
            item['imgs_url'] = imgs_url.strip()
            item['platform'] = "hiapk"
            print "抓取结束，进入pipeline进行数据处理"
            return item
