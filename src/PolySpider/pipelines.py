#!/usr/bin/env python
#coding:gbk

import re
import os
import urllib
import pybcs
from scrapy.exceptions import DropItem
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
from PolySpider.util import CommonUtil
from PolySpider.util import ApkUtil
from PolySpider.util import CategoryUtil
from PolySpider.util import FileUploadUtil

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

'''
执行顺序ID：100
判断版本号，根据版本号来判断是否进行后续操作
'''
class VersionCmpPipeline(object):
    def process_item(self,item,spider):
        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
        #如果表不存在，则创建表
        SqliteUtil.checkAppInfoExist(con)
        oldItem = SqliteUtil.getItemByAppName(con,item['app_name'])
        if oldItem == []:
            print "数据库中无该App记录，执行插入操作"
        elif CommonUtil.cmpVersion(oldItem[0][5], item['version']): 
            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
        return item

'''
执行顺序ID：101
处理应用的分类的Pipeline
'''
class CategorizingPipeline(object):
    def process_item(self,item,spider):
        #如果category中没有这个类 会报错
        item['category'] = CategoryUtil.getCategoryIds(item['category'].encode('gbk','ignore'))
        #TODO 未来添加高级分类判定
        return item

'''
执行顺序ID：102
文件上传到服务器
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
        print '开始本地下载apk： %s ' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        #开始下载
        #调用进度条，传入下载url和文件名称
        #CommonUtil.progressbar(url,'apk/' + name)
        print '下载完成'
        #下载文件至本地 Done
        
        #分析APK文件，获取里面的info_list
        #目前值获取了里面的pakage_name，以后可以增加别的需要的属性
        print '开始分析Apk内容'
        #info_list = ApkUtil.getInfoList(name)
        #item['pakage_name'] = info_list['packageInfo']['orig_package']
        item['pakage_name'] = ''
        print '分析完成'
        #Done
        return item
        
        '''
        #上传至百度云
        bcs = pybcs.BCS('http://bcs.duapp.com/', Config.BAIDU_AK, Config.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(Config.BAIDU_BUCKET)
        #声明一个object
        print '开始上传apk %s 到BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        print "%s\n%s\n%s\n%s\n" %(Config.BAIDU_AK,Config.BAIDU_SK,Config.BAIDU_BUCKET,name)
        obj.put_file('apk/' + name)
        print '上传完成'
        #上传至百度云 Done

        #上传至UpYun
        print '开始上传apk %s 到UpYun' %name
        up = FileUploadUtil.UpYun()
        up.put('apk/' + name, 'apk/' + name)
        print '上传完成'
        #上传至UpYun Done
        '''

'''
执行顺序ID：103
数据库插入或者更新操作
'''
class DatebasePipeline(object):
    def process_item(self,item,spider):
        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
        if SqliteUtil.getItemByAppName(con,item['app_name']) != []:
            #更新数据
            print "数据库更新数据"
            sql = '''
                UPDATE  app_info SET
                    apk_url = ? ,
                    pakage_name = ?,
                    cover = ?,
                    version = ?,
                    rating_star = ?,
                    rating_count = ?,
                    category = ?,
                    android_version = ?,
                    download_times = ?,
                    author = ?,
                    last_update = ?,
                    description = ?,
                    imgs_url = ?,
                    apk_size = ?,
                    platform = ?
                WHERE app_name = ? '''
            data = [(
                item['apk_url'],
                item['pakage_name'],
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
                item['apk_size'],
                item['platform'],
                item['app_name'])]
        else:
            #插入数据
            print '数据库插入数据'
            sql = '''INSERT INTO app_info values(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
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
                    item['apk_size'],
                    item['platform'])]
                    
        SqliteUtil.save_or_update(con, sql, data)
        print '数据库操作结束'
        return item
