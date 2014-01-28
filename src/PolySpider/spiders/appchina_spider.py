#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem

from PolySpider.util import CommonUtil


class AppChinaSpider(CrawlSpider):

    '''
    ##AppChina: 应用汇安卓市场
    *   网址http://www.appchina.com
    *   利用Rule规则进行抓取
    '''
    name = "appchina"
    allowed_domains = ["appchina.com"]
    start_urls = [
        "http://www.appchina.com/"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('www\.appchina\.com/category/', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('www\.appchina\.com/app/.*/$', )),callback='parse_app', follow=True)
    ]

    def parse_app(self, response):
        sel = Selector(response)
        item = AppItem()
        app_china = SpiderConfig.app_china
        if sel.xpath(app_china['app_name']).extract() == []:
            raise DropItem(item)
        print "Grabing Start：%s" % response.url
        # 根据SpiderConfig中的xpath配置进行抓取数据
        for key in app_china:
            value = sel.xpath(app_china[key]).extract() if app_china[key]!='' else ''
            item[key] = value[0].strip().encode('utf8') if len(value) == 1 else ('' if len(value) == 0 else value)
#        try:
            # 应用汇对apk的下载链接做了一层redirect,所以需要更早请求来获取真实下载地址
        res = urllib2.urlopen(item['apk_url'])
        item['apk_url'] = res.url
        # 格式化
        item['app_name'] = CommonUtil.dropBrackets(item['app_name'])
        item['version'] = CommonUtil.normalizeVersion(item['version'])
        item['rating_count'] = item['rating_count'][6:-1]
        item['android_version'] = item['android_version'][9:-4]
        item['download_times'] = CommonUtil.download_time_normalize(item['download_times'])
        item['last_update'] = CommonUtil.normalizeString(item['last_update'])[5:]
        item['description'] = ' '.join(unicode(item['description'])).decode('utf8')
        item['apk_size'] = CommonUtil.normalizeString(item['apk_size'])[5:]
        # 获取图片地址，通过空格来分割多张图片
        item['imgs_url'] = " ".join(item['imgs_url'])
        item['platform'] = "appchina"
        print "Grabing finish, step into information pipline"
        return item
#        except Exception:
#            raise DropItem(item)


#        try:
#            sel = Selector(response)
#            item = AppItem()
#            print "Grabing Start：%s" %response.url
#            if len(sel.xpath('//div[@class="down-box cf"]/a[3]/@href').extract())==0:
#                item['app_name']=""
#                return item
#            else:
# 应用汇对apk的下载链接做了一层redirect,所以需要更早请求来获取真实下载地址
#                apk_url =  sel.xpath('//div[@class="down-box cf"]/a[3]/@href').extract()[0]
#                response= urllib2.urlopen(apk_url)
#                item['apk_url'] = response.url
#                item['app_name'] = CommonUtil.dropBrackets(sel.xpath("//h1[@class='ch-name cutoff fl']/text()").extract()[0].strip())
#                item['cover'] = sel.xpath('//div[@class="cf"]/img/@src').extract()[0]
#                item['version'] = CommonUtil.normalizeVersion(CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/div[2]/p[1]/text()').extract()[0]))
# item['rating_point'] = ""#应用汇没有评分，志愿后评价人数
#                item['rating_count'] = sel.xpath('//a[@class="linkmore"]/text()').extract()[0][6:-2]
#                item['category'] = sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[3]/a/text()').extract()[0]
#                item['android_version'] = sel.xpath('//*[@id="app-detail-wrap"]/div[1]/span[@class="sys"]/text()').extract()[0].replace('\n','')[7:-2].strip()
#                item['download_times']=CommonUtil.download_time_normalize(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[2]/em/text()').extract()[0])
#                author=sel.xpath('//span[@class="dl authon-name"]/text()').extract()
#                if len(author)==0:
#                    author = ''
#                item['author'] = author[0]
#                item['last_update'] = CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[4]/text()').extract()[0])[5:]
#                descriptions = sel.xpath('//*[@id="scrollbar1"]/div[2]/div/div/text()').extract()
#                destemp=''
#                for des in descriptions:
#                    destemp=destemp+des+' '
#                item['description']=CommonUtil.normalizeString(destemp)
#                item['apk_size'] = CommonUtil.normalizeString(sel.xpath('//*[@id="app-detail-wrap"]/div[2]/ul/li[1]/text()').extract()[0])[5:]
# 获取图片地址，通过空格来分割多张图片
#                imgs = sel.xpath('//*[@id="makeMeScrollable"]/a/@href').extract()
#                imgs_url = ""
#                for img in imgs: imgs_url += img + " "
#                item['imgs_url'] = imgs_url.strip()
#                item['platform'] = "appchina"
#                print "Grabing finish, step into information pipline"
#                return item
#        except HTTPError:
#            item['app_name']=""
#            return item
