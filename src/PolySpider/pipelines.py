#!/usr/bin/env python
#coding:gbk

from PolySpider import Config
from PolySpider import SqliteUtils
from PolySpider import CommonUtils
from PolySpider import apkParser
from scrapy.exceptions import DropItem
from PolySpider import CategoryUtils
from PolySpider import FileUploadUtils
import re
import os
import urllib
import pybcs

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

'''
执行顺序ID：100
判断版本号，根据版本号来判断是否进行后续操作
'''
class VersionCmpPipeline(object):
    def process_item(self,item,spider):
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)
        cur = SqliteUtils.get_cursor(con)
        #如果表不存在，则创建表
        SqliteUtils.checkAppInfoExist(con)
        oldItem = SqliteUtils.getItemByAppName(cur,item['app_name'])
        if oldItem != [] and CommonUtils.cmpVersion(oldItem[0][5], item['version']): 
            print "Crawled app has been record in databse. No newer version has been found!"
            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
        return item

'''
执行顺序ID：101
处理应用的分类的Pipeline
'''
class CategorizingPipeline(object):
    def process_item(self,item,spider):
        #如果category中没有这个类 会报错
        a=item['category'].encode('gbk','ignore')
        print "Grab CategoryName: %s" %a
        item['category'] = CategoryUtils.getCategoryIds(a)
        #TODO 未来添加高级分类判定
        return item

'''
执行顺序ID：102
文件下载到服务器
分析Apk信息
上传到UpYun/BaiduYun
'''
class FileUploadPipeline(object):
    def process_item(self,item,spider):
        url = item['apk_url']
        
        ##根据获取的apk下载地址将apk文件传至百度云
        #正则匹配文件名
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #下载文件至本地
        print 'Start Download apk %s locally' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        #开始下载
        print "Begin to download "+name
        #调用进度条，传入下载url和文件名称
        #CommonUtils.progressbar(url,'apk/' + name)
        print 'Download Finished'
        #下载文件至本地 Done
        
        #分析APK文件，获取里面的info_list
        #目前值获取了里面的pakage_name，以后可以增加别的需要的属性
        #info_list = apkParser.getInfoList(name)
        #item['pakage_name'] = info_list['packageInfo']['orig_package']
        item['pakage_name'] = ''
        #Done
        return item
        
        '''
        #上传至百度云
        bcs = pybcs.BCS('http://bcs.duapp.com/', Config.BAIDU_AK, Config.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(Config.BAIDU_BUCKET)
        #声明一个object
        print 'Start Upload apk %s to BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        print "%s\n%s\n%s\n%s\n" %(Config.BAIDU_AK,Config.BAIDU_SK,Config.BAIDU_BUCKET,name)
        obj.put_file('apk/' + name)
        print 'Upload Finished'
        #上传至百度云 Done
        '''
'''
        #上传至UpYun
        up = FileUploadUtils.UpYun()
        up.put('apk/' + name, 'apk/' + name)
        #上传至UpYun Done

        
'''
'''
执行顺序ID：103
数据库插入或者更新操作
'''
class DatebasePipeline(object):
    def process_item(self,item,spider):
        
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)
        
        #插入数据
        sql_insert = '''
            INSERT INTO app_info values(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        data = [(
                item['apk_url'],
                item['pakage_name'],
                item['app_name'],
                item['cover'],
                item['version'],
                item['rating_star'],
                item['rating_count'],
                item['category'],
                item['android_version'],
                item['download_times'],
                item['author'],
                item['last_update'],
                item['description'],
                item['imgs_url'],
                item['apksize'])]
        SqliteUtils.save_or_update(con, sql_insert, data)
        return item
