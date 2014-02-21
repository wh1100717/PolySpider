#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
import urllib
import re
from scrapy.selector import Selector
from PolySpider.items import AppItem
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem

from PolySpider.util import CommonUtil

class HiapkSpider(Spider):
    '''
    ##Hiapk: 安卓市场
    *   网址http://apk.hiapk.com/
    *   因为其大部分的category都是用动态请求的方式来获取的，所以直接通过rule是抓不到的，分析其动态请求并构造request进行应用抓取
    '''
    name = "hiapk"
    allowed_domains = ["hiapk.com"]
    start_urls = [
        "http://apk.hiapk.com/apps",
        "http://apk.hiapk.com/games"
    ]
    def parse(self,response):
        '''
        *   如果url满足第一个条件，则说明是应用详细页，则对其进行数据抓取
        *   如果url满足第二个条件，则说明是分类列表页，则分析里面的url并构造request
        '''
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
            #TODO 需要看看如何修改该请求，现在一次性构造请求太多，太耗费资源。
            for app_category in apps_categories: 
                for a in range(1,100):
#                    for b in range(1,4):
#                        for c in [0,1,2,4]:
#                            for d in [0,1,2]:
#                                for e in range(4):
#                                    for f in range(6):
#                                        for g in range(4): 
                    url = 'http://apk.hiapk.com/App.aspx?action=FindAppSoftList'
                    currentHash=str(a)+"_1_0_0_0_0_0"
                    req=urllib2.Request(url)
                    data=urllib.urlencode(dict(categoryId=app_category.split('_')[1],currentHash=currentHash))
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                    response_content = opener.open(req, data)
                    content=response_content.read()
                    url_lists=re.findall("http://apk.hiapk.com/html/\d{4}/\d{2}/\d+\.html",content)
                    if len(url_lists)==0:
                        break
                    else:
                        for url_list in url_lists:
                            yield Request(url_list,callback = self.parse_app)
    def return_item(self, item):
        return item
    def parse_app(self, response):
        sel = Selector(response)
        item = AppItem()
        hiapk = SpiderConfig.hiapk
        print "Grabing Start：%s" % response.url
        # 根据SpiderConfig中的xpath配置进行抓取数据
        for key in hiapk:
            value = sel.xpath(hiapk[key]).extract() if hiapk[key]!='' else ''
            item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
        print item['apk_url']
        req=urllib2.Request("http://apk.hiapk.com" +item['apk_url'])
        req.add_header('referer', response.url)
        item['apk_url'] = urllib2.urlopen(req).url
        android_version = item['android_version'].replace('及以上固件版本',"+") 
        item['android_version'] =android_version[0:android_version.find('至')]
        item['package_name']=item['package_name'].split('=')[3].split(';')[0].strip()[1:-1]
        if len(item['rating_point']) < 21:
            item['rating_point'] = "0"
            item['rating_count'] = "0"
        else:
            item['rating_point'] = item['rating_point'][21:-2] if len(item['rating_point']) > 21 else "0"
            if "half" in item['rating_point']: item['rating_point'] = item['rating_point'][0] + ".5"
            
            if len(item['rating_count'])==0:
                item['rating_count']=''
            else:
                item['rating_count'] = item['rating_count'][:-3]
        item['imgs_url']=' '.join(item['imgs_url'])
        item['platform'] = "hiapk"
        print "Grabing finish, step into information pipline"
        return item
#        try:
#            print "Grabing Start：%s" %response.url
#            req=urllib2.Request("http://apk.hiapk.com" +   sel.xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href').extract()[0])
#            req.add_header('referer', response.url)
#            item['apk_url'] = urllib2.urlopen(req).url
#            item['app_name'] = CommonUtil.dropBrackets(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()').extract()[0])
#            item['cover'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src').extract()[0]
#            item['version'] =CommonUtil.normalizeVersion(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()').extract()[0])
#            item['category'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()').extract()[0]
#            android_version = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()').extract()[0].replace('及以上固件版本',"+") 
#            item['android_version'] =android_version[0:android_version.find('至')]
#            item['download_times'] = CommonUtil.download_time_normalize(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()').extract()[0])
#            author =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()
#            item['author'] = '' if len(author)==0 else author[0]
#            item['last_update'] =   sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftPublishTime"]/text()').extract()[0]
#            description=sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()').extract()
#            if len(description)==0:
#                description =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/p/text()').extract()[0]
#            else:
#                description =  description[0]
#            item['description']=description.strip()
#            item['apk_size'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSize"]/text()').extract()[0]
#            rating_star = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/@class').extract()[0]
#            if len(rating_star) < 21:
#                item['rating_point'] = "0"
#                item['rating_count'] = "0"
#            else:
#                item['rating_point'] = rating_star[21:-2] if len(rating_star) > 21 else "0"
#                if "half" in item['rating_point']: item['rating_point'] = item['rating_point'][0] + ".5"
#                rating_count=sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()').extract()
#                if len(rating_count)==0:
#                    item['rating_count']=''
#                else:
#                    item['rating_count'] = rating_count[0][:-3]
#            #获取图片地址，通过空格来分割多张图片
#            imgs =  sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href').extract()
#            imgs_url = ""
#            for img in imgs: imgs_url += img + " "
#            item['imgs_url'] = imgs_url.strip()
#            item['platform'] = "hiapk"
#            print "Grabing finish, step into information pipline"
#            return item
#        except HTTPError:
#            item['app_name']=""
#            return item