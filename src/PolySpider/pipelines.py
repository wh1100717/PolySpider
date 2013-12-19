#!/usr/bin/env python
#coding:gbk

from PolySpider import settings
import pybcs, re, urllib

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item
    
class AppStarSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'app_star': return item
        url = item['apk_url']
        
        ##根据获取的apk下载地址将apk文件传至百度云
        
        #正则匹配文件名
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #下载文件到本地
        print 'Start Download apk %s locally' %name
        urllib.urlretrieve(url, 'apk/' + name)
        print 'Download Finished'
        #上传至百度云
        bcs = pybcs.BCS('http://bcs.duapp.com/', settings.BAIDU_AK, settings.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(settings.BAIDU_BUCKET)
        #声明一个object
        print 'Start Upload apk %s to BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        obj.put_file('apk/' + name)
        print 'Upload Finished'
        return item
