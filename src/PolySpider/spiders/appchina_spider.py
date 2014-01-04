#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem

from PolySpider.util import CommonUtil

class AppStarSpider(CrawlSpider):
	name = "appchina"
	allowed_domains = ["appchina.com"]
	start_urls = [
                "http://www.appchina.com/"        
	]
       # rules = [Rule(SgmlLinkExtractor(allow=("http\://apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )), callback='parse_app'),]
  
        rules = [
                Rule(SgmlLinkExtractor(allow=('www\.appchina\.com', )),follow=True),
		Rule(SgmlLinkExtractor(allow=('www\.appchina\.com/app/.*/$', )),callback='parse_app',follow=True)
	]
	def parse_app(self, response):	
		sel = Selector(response)
                item = AppItem()
                print "抓取开始：%s" %response.url
                apk_url =  sel.xpath('//div[@class="down-box cf"]/a[3]/@href').extract()[0]
                response= urllib2.urlopen(apk_url)
                item['apk_url'] = response.url
                item['app_name'] = CommonUtil.dropBrackets(sel.xpath("//h1[@class='ch-name cutoff fl']/text()").extract()[0].strip())
                item['cover'] = sel.xpath('//div[@class="cf"]/img/@src').extract()[0]
                item['version'] = CommonUtil.normalizeVersion(CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/div[2]/p[1]/text()').extract()[0]))
                item['rating_star'] = ""
                item['rating_count'] = sel.xpath('//a[@class="linkmore"]/text()').extract()[0][6:-2]
                item['category'] = sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[3]/a/text()').extract()[0]
                item['android_version'] = sel.xpath('//*[@id="app-detail-wrap"]/div[1]/span[@class="sys"]/text()').extract()[0].replace('\n','')[7:-2].strip()
                item['download_times']=sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[2]/em/text()').extract()[0]
                item['author'] = sel.xpath('//span[@class="dl authon-name"]/text()').extract()[0]
                item['last_update'] = CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[4]/text()').extract()[0])[5:]
                descriptions = sel.xpath('//*[@id="scrollbar1"]/div[2]/div/div/text()').extract()
                destemp=''
                for des in descriptions:
                    destemp=destemp+des+' '
                item['description']=CommonUtil.normalizeString(destemp)
                item['apk_size'] = CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[1]/text()').extract()[0])[5:]
                #获取图片地址，通过空格来分割多张图片
                imgs = sel.xpath('//*[@id="makeMeScrollable"]/a/@href').extract()
                imgs_url = ""
                for img in imgs: imgs_url += img + " "
                item['imgs_url'] = imgs_url.strip()
                item['platform'] = "appchina"
                print "抓取结束，进入pipeline进行数据处理"
		return item
