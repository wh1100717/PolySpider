#!/usr/bin/env python
#coding:gbk

from PolySpider import Config
from PolySpider import SqliteUtils
import pybcs
import re
import urllib
import upyun
import os

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class AppStarFileUploadPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'app_star': return item
        url = item['apk_url']
        
        ##根据获取的apk下载地址将apk文件传至百度云
        #正则匹配文件名
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #下载文件至本地
        print 'Start Download apk %s locally' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        urllib.urlretrieve(url, 'apk/' + name)
        print 'Download Finished'
        #下载文件至本地 Done
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
        # 参数 `bucket` 为空间名称,`username` 和 `password` 分别为授权操作员帐号和密码，必选。
        # 参数 `timeout` 为 HTTP 请求超时时间，默认 60 秒，可选。
        # 根据国内的网络情况，又拍云存储 API 目前提供了电信、联通网通、移动铁通三个接入点，
        # 在初始化时可由参数 `endpoint` 进行设置，其可选的值有：
        # upyun.ED_AUTO     根据网络条件自动选择接入点，默认
        # upyun.ED_TELECOM  电信接入点
        # upyun.ED_CNC      联通网通接入点
        # upyun.ED_CTT      移动铁通接入点

        up = upyun.UpYun(Config.UPYUN_BUCKET, Config.UPYUN_USERNAME, Config.UPYUN_PASSWORD, timeout=30, endpoint=upyun.ED_AUTO)
        print "Bucket:%s | UserName:%s" %(Config.UPYUN_BUCKET, Config.UPYUN_USERNAME)
        up.put('/apk/' + name, 'apk/' + name)
        #上传至UpYun Done
        '''
        
        return item
class AppStarDatabasePipeline(object):
    def process_item(self, item, spider):
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)
        cur = SqliteUtils.get_cursor(con)

        #如果表不存在，则创建表
        if  not SqliteUtils.is_table_exist(cur, 'app_info'):
            sql_table_create = '''
                CREATE TABLE app_info(
                id INTEGER PRIMARY KEY,
                apk_url VARCHAR(32))
            '''
            SqliteUtils.create_table(con,sql_table_create)
        #插入数据
        sql_insert = '''
            INSERT INTO app_info values(null,?)
        '''
        data = [(item['apk_url'],)]
        SqliteUtils.save_or_update(con, sql_insert, data)
        return item
