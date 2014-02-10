#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider.util import CommonUtil
from PolySpider.config import SpiderConfig
from scrapy.exceptions import DropItem
class MZWSpider(CrawlSpider):
   
    name = "muzhiwan"
    allowed_domains = ["muzhiwan.com"]
    start_urls = [
        "http://www.muzhiwan.com/category/",
        "http://www.muzhiwan.com/wangyou/fenlei/"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=('muzhiwan\.com/[^/]*\.html$', )),callback='parse_app',follow=True),
        Rule(SgmlLinkExtractor(allow=('category/\d.*/','-0-0-\d.*')), follow = True),
    ]
    def parse_app(self, response):
#        try:
        sel = Selector(response)
        item = AppItem()
        muzhiwan=SpiderConfig.muzhiwan
        print "Grabing Start：%s" %response.url
        for key in muzhiwan:
            value = sel.xpath(muzhiwan[key]).extract() if muzhiwan[key]!='' else ''
            item[key] = value[0].strip() if len(value) == 1 else ('' if len(value) == 0 else value)
        item['rating_count']=item['rating_count'][2:-2]
        item['android_version'] =item['android_version'].replace('适用：Android','').replace('以上','').strip()
        item['last_update']=item['last_update'].replace('发布：','')
        item['apk_size']=item['apk_size'].replace('大小：','')
        item['description']=' '.join(item['description'])
        item['imgs_url']=' '.join(item['imgs_url'])
        item['platform'] = "muzhiwan"
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