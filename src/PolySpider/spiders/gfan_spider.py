#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider.util import CommonUtil
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem
class GfanSpider(CrawlSpider):
   
    name = "gfan"
    allowed_domains = ["gfan.com"]
    start_urls = [
        "http://apk.gfan.com/apps_7_1_1.html",
        "http://apk.gfan.com/games_8_1_1.html"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('App\d.*', )),callback='parse_app',follow=True),
        Rule(SgmlLinkExtractor(allow=('\b.*_\d.*_\d.*_\d.*' )), follow = True),
    ]
    def parse_app(self, response):
#        try:
        sel = Selector(response)
        item = AppItem()
        gfan=SpiderConfig.gfan
        print "Grabing Start：%s" %response.url
        for key in gfan:
            value = sel.xpath(gfan[key]).extract() if gfan[key]!='' else ''
            item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
        item['version']=item['version'][-3:]
        item['rating_count']=item['rating_count'][3:item['rating_count'].find('(')]
        item['android_version'] =item['android_version'].replace('支持固件：','').replace('及以上版本','').strip()
        item['author']=item['author'].replace('开 发 者：','')
        item['last_update']=item['last_update'].replace('发布时间：','')
        item['apk_size']=item['apk_size'].replace('文件大小：','')
        item['description']=' '.join(item['description'])
        item['imgs_url']=' '.join(item['imgs_url'])
        item['platform'] = "gfan"
        print "Grabing finish, step into information pipline"
        return item
#            apk_url = sel.xpath('//*[@id="down_as_durl"]/@href').extract()
#            if len(apk_url)==0:
#                item['app_name']=''
#                return item
#            else:
#                item['apk_url'] = apk_url[0]
#                item['app_name'] = CommonUtil.dropBrackets(sel.xpath("//*[@id='appname']/text()").extract()[0])
#                item['cover'] = sel.xpath("//*[@id='app-logo']/@src").extract()[0]
#                item['version'] = CommonUtil.normalizeVersion(sel.xpath("//*/td[2]/span/text()").extract()[0])
#                item['rating_point'] = sel.xpath("//*[@id='score-num']/text()").extract()[0][:-1]
#                item['rating_count'] = sel.xpath("//*[@id='score-participants']/text()").extract()[0][3:-4]
#                item['category'] =  sel.xpath("//span[@class='params-catename']/text()").extract()[0]
#                item['android_version'] =sel.xpath("//*/tr[2]/td[2]/span/text()").extract()[0][7:-3]
#                item['download_times'] = CommonUtil.download_time_normalize(sel.xpath("//*/tr[2]/td[1]/span/text()").extract()[0])
#                item['author'] =  ''
#                item['last_update'] =   sel.xpath("//*/tr[3]/td[1]/span/text()").extract()[0]
#                descriptions = sel.xpath("//*[@class='brief-des']/text()").extract()
#                destemp=''
#                for des in descriptions:
#                    destemp=destemp+des+' '
#                item['description']=destemp.strip()
#                item['apk_size'] = sel.xpath('//span[@class="params-size"]/text()').extract()[0]
#                #获取图片地址，通过空格来分割多张图片
#                imgs =  sel.xpath("//ul[@class='screen cls data-screenshots']/li/img/@src").extract()
#                imgs_url = ""
#                for img in imgs: imgs_url += img + " "
#                item['imgs_url'] = imgs_url.strip()
#                item['platform'] = "baiduapp"
#                print "Grabing finish, step into information pipline"
#                return item
#        except HTTPError:
#            item['app_name']=""
#            return item