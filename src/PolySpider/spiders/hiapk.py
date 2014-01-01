#!/usr/bin/env python
#coding:gbk
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider import CommonUtils
import urllib2
class AppStarSpider(CrawlSpider):
	name = "hiapk"
	allowed_domains = ["hiapk.com"]
	start_urls = [
                "http://apk.hiapk.com/apps"
	]
       # rules = [Rule(SgmlLinkExtractor(allow=("http\://apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )), callback='parse_app'),]
        rules = [
		Rule(SgmlLinkExtractor(allow=('/[0-9]*/[0-9]*/[0-9]*\.html', )),callback='parse_app',follow=True)
	]
	def parse_app(self, response):	

            sel = Selector(response)
            item = AppItem()
            print "抓取开始：%s" %response.url
            downloadlink = "http://apk.hiapk.com" +   sel.xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href').extract()[0]
            req=urllib2.Request(downloadlink)
            req.add_header('referer', response.url)
            response=urllib2.urlopen(req)

            item['apk_url'] = response.url
            name = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()').extract()[0]
            item['app_name'] = name


            item['cover'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src').extract()[0]
            item['version'] = CommonUtils.normalizeVersion(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()').extract()[0])
            item['category'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()').extract()[0]
            item['android_version'] =sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()').extract()[0]
            item['download_times'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()').extract()[0]
            item['author'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()[0]
            item['last_update'] =   sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftPublishTime"]/text()').extract()[0]
            item['description'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()').extract()[0]
            item['apk_size'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSize"]/text()').extract()[0]
            item['rating_count'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()').extract()[0][:-3]
            item['rating_star'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/@class').extract()[0][21:-2]
            if "half" in item['rating_star']: item['rating_star'] = item['rating_star'][0] + ".5"
            #获取图片地址，通过空格来分割多张图片
            imgs =  sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href').extract()
            imgs_url = ""
            for img in imgs: imgs_url += img + " "
            item['imgs_url'] = imgs_url.strip()
            print "抓取结束，进入pipeline进行数据处理"
            return item
