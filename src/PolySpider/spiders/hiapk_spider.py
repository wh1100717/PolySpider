#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
import re
from scrapy.selector import Selector
from PolySpider.items import AppItem
from scrapy.http import Request,FormRequest
from scrapy.spider import BaseSpider

from PolySpider.util import CommonUtil

class HiapkSpider(BaseSpider):
	name = "hiapk"
	allowed_domains = ["hiapk.com"]
	start_urls = [
                "http://apk.hiapk.com/apps",
                "http://apk.hiapk.com/games",
	]
        def parse(self,response):
            if re.match(r".*/html/\d{4}/\d{2}/\d+\.html",response.url):
                item = self.parse_app(response)
                yield self.return_item(item)
            elif re.match(ur"http\://.*SoftList",response.url):
                sel = Selector(response)
                urls = sel.xpath('//li/dl/dt/span/a/@href').extract()
                for url in urls:
                    yield Request(url,callback = self.parse_app)
            else:
                apps_categories=[
                    'apps_281_1_1','apps_52_1_1','apps_285_1_1','apps_282_1_1','apps_71_1_1','apps_283_1_1',
                    'apps_37_1_1','apps_42_1_1','apps_284_1_1','apps_39_1_1','apps_287_1_1','apps_286_1_1',
                    'apps_46_1_1','apps_35_1_1','apps_36_1_1','apps_40_1_1','apps_49_1_1','apps_45_1_1',
                    'apps_31_1_1','apps_289_1_1','apps_291_1_1','apps_290_1_1','apps_29_1_1','apps_81_1_1',
                    'apps_30_1_1','apps_80_1_1','apps_292_1_1','apps_79_1_1','apps_288_1_1'
                    ]
                index=1
                for app_category in apps_categories:

#                    for a in range(1,101):
#                        for b in range(1,4):
#                            for c in [0,1,2,4]:
#                                for d in [0,1,2]:
#                                    for e in range(4):
#                                        for f in range(6):
#                                            for g in range(4): 
#                    
#                                                url = 'http://apk.hiapk.com/App.aspx?action=FindAppSoftList&'+str(index)
#                                                currentHash=str(a)+"_"+str(b)+"_"+str(c)+"_"+str(d)+"_"+str(e)+"_"+str(f)+"_"+str(g)
#                                                index+=1
#                                                yield FormRequest(url,formdata={"currentHash":currentHash,"categoryId":app_category.split("_")[1]},headers={"referer":"http://apk.hiapk.com/"+app_category,"host":"apk.hiapk.com","Origin":"http://apk.hiapk.com"})
                    url = 'http://apk.hiapk.com/App.aspx?action=FindAppSoftList&'+str(index)
                    currentHash=str(1)+"_"+str(1)+"_"+str(0)+"_"+str(0)+"_"+str(0)+"_"+str(0)+"_"+str(0)
                    index+=1
                    yield FormRequest(url,formdata={"currentHash":currentHash,"categoryId":app_category.split("_")[1]},headers={"referer":"http://apk.hiapk.com/"+app_category,"host":"apk.hiapk.com","Origin":"http://apk.hiapk.com"})
        def return_item(self, item):
            return item
           
	def parse_app(self, response):	
            sel = Selector(response)
            item = AppItem()
            print "抓取开始：%s" %response.url
            req=urllib2.Request("http://apk.hiapk.com" +   sel.xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href').extract()[0])
            req.add_header('referer', response.url)

            item['apk_url'] = urllib2.urlopen(req).url
            item['app_name'] = CommonUtil.dropBrackets(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()').extract()[0])
            item['cover'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src').extract()[0]
            item['version'] =CommonUtil.normalizeVersion(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()').extract()[0])
            item['category'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()').extract()[0]
            item['android_version'] =sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()').extract()[0]
            item['download_times'] = CommonUtil.download_time_normalize(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()').extract()[0])
            author =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()
            if len(author)==0:
                author = ''
            else:
                author = author[0]
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
                item['rating_point'] = "0"
                item['rating_count'] = "0"
            else:
                item['rating_point'] = rating_star[21:-2] if len(rating_star) > 21 else "0"
                if "half" in item['rating_point']: item['rating_point'] = item['rating_point'][0] + ".5"
                rating_count=sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()').extract()
                if len(rating_count)==0:
                    item['rating_count']=''
                else:
                    item['rating_count'] = rating_count[0][:-3]
            #获取图片地址，通过空格来分割多张图片
            imgs =  sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href').extract()
            imgs_url = ""
            for img in imgs: imgs_url += img + " "
            item['imgs_url'] = imgs_url.strip()
            item['platform'] = "hiapk"
            print "抓取结束，进入pipeline进行数据处理"
            return item
