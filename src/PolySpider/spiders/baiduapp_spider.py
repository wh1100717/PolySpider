#!/usr/bin/env python
#coding:gbk
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from PolySpider.items import AppItem
from PolySpider import Config
import urllib2
class AppStarSpider(CrawlSpider):
	name = "baidu"
	allowed_domains = ["baidu.com"]
	start_urls = [
                "http://as.baidu.com/a/software?cid=101&s=1&f=home_2005_1"
	]
       # rules = [Rule(SgmlLinkExtractor(allow=("http\://apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )), callback='parse_app'),]
        rules = [
		Rule(SgmlLinkExtractor(allow=('item\?docid=\d.*', )),callback='parse_app',follow=True)
	]
	def parse_app(self, response):	
		sel = Selector(response)
                item = AppItem()
                
                item['apk_url'] = sel.xpath('//*[@id="down_as_durl"]/@href').extract()[0]
		
                item['app_name'] = sel.xpath("//*[@id='appname']/text()").extract()[0]
            
                item['cover'] = sel.xpath("//*[@id='app-logo']/@src").extract()[0]
                item['version'] = sel.xpath("//*/td[2]/span/text()").extract()[0]
                item['rating_star'] = sel.xpath("//*[@id='score-num']/text()").extract()[0]
                item['rating_count'] = sel.xpath("//*[@id='score-participants']/text()").extract()[0][3:-4]
                item['category'] =  sel.xpath("//span[@class='params-catename']/text()").extract()[0]
                item['android_version'] =sel.xpath("//*/tr[2]/td[2]/span/text()").extract()[0]
                item['download_times'] = sel.xpath("//*/tr[2]/td[1]/span/text()").extract()[0]
                item['author'] =  ''
                item['last_update'] =   sel.xpath("//*/tr[3]/td[1]/span/text()").extract()[0]

                item['description'] =  sel.xpath("//*[@class='brief-des']/text()").extract()[:5]
                item['apksize'] = sel.xpath('//span[@class="params-size"]/text()').extract()[0]
                #获取图片地址，通过空格来分割多张图片
                imgs =  sel.xpath("//ul[@class='screen cls data-screenshots']/li/img/@src").extract()
                imgs_url = ""
                for img in imgs: imgs_url += img + " "
                item['imgs_url'] = imgs_url.strip()
		return item
