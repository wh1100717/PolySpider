#!/usr/bin/env python
#coding:gbk
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider import CommonUtils
from PolySpider.items import AppItem
import urllib2
class AppStarSpider(CrawlSpider):
	name = "appchina"
	allowed_domains = ["appchina.com"]
	start_urls = [
                "http://www.appchina.com/category/30.html"
	]
       # rules = [Rule(SgmlLinkExtractor(allow=("http\://apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )), callback='parse_app'),]
  
        rules = [
		Rule(SgmlLinkExtractor(allow=('appdetail.jsp?appid=', )),callback='parse_app',follow=True)
	]
	def parse_app(self, response):	
		sel = Selector(response)
                item = AppItem()
                apk_url =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[5]/a[2]/@href').extract()[0]
                response= urllib2.urlopen(apk_url)

                item['apk_url'] = response.url
		
                item['app_name'] = sel.xpath("//h1[@class='ch-name cutoff fl']/text()").extract()[0]
            
                item['cover'] = sel.xpath('/html/body/div[3]/div[2]/article/header/div[1]/img/@src').extract()[0]
                item['version'] = sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[6]/text()').extract()[0]
                item['rating_star'] = sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/div[1]/span[1]/span/text()').extract()[0]
                item['rating_count'] =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/div[1]/span[2]/text()').extract()[0][:-3]
                item['category'] =   sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[4]/text()').extract()[0]
                item['android_version'] = sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[8]/text()').extract()[0]
                item['download_times'] =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[1]/text()').extract()[0].replace(',','')
                item['author'] =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[9]/text()').extract()[0]
                item['last_update'] =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[7]/time/text()').extract()[0]
                descriptions = sel.xpath('/html/body/div[3]/div[2]/article/section[1]/p/text()').extract()
                for des in descriptions:
                    item['description']=item['description']+des+' '
              
                item['apk_size'] =  sel.xpath('/html/body/div[3]/div[2]/article/header/div[2]/dl/dd[2]/text()').extract()[0]
                #获取图片地址，通过空格来分割多张图片
                imgs =  sel.xpath('/html/body/div[3]/div[2]/article/section[3]/div/div/div/img/@src').extract()
                imgs_url = ""
                for img in imgs: imgs_url += img + " "
                item['imgs_url'] = imgs_url.strip()
		return item
