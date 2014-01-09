#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import re
import os
from scrapy.exceptions import DropItem
from PolySpider.util import CategoryUtil
from PolySpider.util import SqliteUtil
from PolySpider.sql import App
from PolySpider.sql import AppDetail
from PolySpider.sql import Status

import urllib
import pybcs
from PolySpider.util import ApkUtil
from PolySpider.util import FileUploadUtil
from PolySpider.util import CommonUtil
from PolySpider.config import Config




class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class CategorizingPipeline(object):
    '''
    执行顺序ID：100
    处理应用的分类的Pipeline~
    '''
    def process_item(self,item,spider):
        #判断item是否为空，如果为空，则drop item
        if not item or item['app_name'] == "":  
            raise DropItem(item)
        #如果category中没有这个类 会报错
        item['category'] = CategoryUtil.get_category_id_by_name(item['category'].encode('utf8','ignore'))
        item['DROP_APP'] = False
        item['NEW_APP'] = False
        item['UPDATE_APP'] = False
        return item

class CheckAppPipeline(object):
    '''
    执行顺序ID：101
    检查ps_app表中是否存在该App数据
    如果不存在，则记录该App数据
    如果存在，检查author,如果为空，则更新author
    '''
    def process_item(self,item,spider):
        SqliteUtil.checkTableExist()
        app_name = item['app_name']
        app = App.get_app_by_app_name(app_name)
        
        if not app:
            #构造分类
            temp=""
            for category in item['category'].split(","):
                temp = temp + category + ":1,"
            
            item['category']=temp[:-1]
            #插入数据
            item['app_id'] = App.insert_app(item)
            item['NEW_APP'] = True
        else:
            app = app[0]
            item['app_id'] = app[0]
            item['app_category'] = app[3]
            item['UPDATE_APP'] = True
            #更新分类
            #判断author是否为空，如果为空，则更新app表
            if app[2] == "" and item['author'] != "":
                App.update_app_author(app[0], item['author'])
        return item

class CheckAppDetailsPipeline(object):
    '''
    执行顺序ID：102
    分析ps_app_detail表中是否存在该App_Detail数据(通过app_id, verison, flatform做唯一标识)
    如果不存在，则记录该App数据
    如果存在，更新一些数据信息，然后将该ItemDrop掉
    '''
    def process_item(self,item,spider):
        app_detail = AppDetail.get_app_detail_by_item(item)
        if not app_detail:
            #下载Apk | 分析Apk并记录pakage_name | 上传Apk至UpYun
            self.apk_operation(item)
            #插入数据
            AppDetail.insert_app_detail(item)
        else:
            #TODO 可能涉及到更新操作-->rating_point | rating_count | download_times | apk_url | cover | 
            item['DROP_APP'] = True
        return item
        
    def apk_operation(self, item):
        '''
        执行顺序ID：102
        文件上传到服务器
        分析Apk信息,获取pakage_name
        上传到UpYun/BaiduYun
        '''
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

class UpdateCategoryPipeline(object):
    '''
    执行顺序ID：103
    更新ps_app中的category项
    '''
    def process_item(self,item,spider):
        
        if item['DROP_APP']: return item
        if not item['NEW_APP']:
            #重新计算category
            item_category = item['category']
            print item['category']#2200,3800
            print item['app_category']#2200:1,3800:1,
            categories = item['app_category'].split(",")
            flag = True
            for index in range(len(categories)):
                category = categories[index]#2200:1
                app_category_name = category[:category.find(":")]#2200
                if app_category_name in item_category:
                    categories[index] = app_category_name + ":" + str(int(category[(category.find(":") + 1):]) + 1)
                    item['app_category'] = ",".join(self.category_reorder(categories))
                    flag = False
                    break
            if flag:
                item['app_category'] = item['app_category'] + "," + item['category'] + ":1"
            #更新ps_app表的category
            App.update_app_category(item['app_id'], item['app_category'])
        return item
    
    def category_reorder(self,categories):
        length = len(categories)
        for i in range(length):
            order_category = categories[i]
            order_category_value = int(order_category[(order_category.find(":")+1):])
            for j in range(1,length-i):
                cmp_category = categories[j]
                cmp_category_value = int(cmp_category[(cmp_category.find(":")+1):])
                if cmp_category_value > order_category_value:
                    categories[i],categories[j] = categories[j],categories[i]
        return categories

class StatusRecordPipeline(object):
    '''
    执行顺序ID：104
    更新ps_status记录
    '''
    def process_item(self, item, spider):
        status = Status.get_today_status(item['platform'])
        data = [(status[3] + 1, status[4] + 1 if item['NEW_APP'] else status[4], status[5] + 1 if item['UPDATE_APP'] else status[5], status[0])]
        Status.update_status(data)
        return item


#'''
#执行顺序ID：100
#判断版本号，根据版本号来判断是否进行后续操作
#'''
#class VersionCmpPipeline(object):
#    def process_item(self,item,spider):
#        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
#        #如果表不存在，则创建表
#        SqliteUtil.checkAppInfoExist(con)
#        oldItem = SqliteUtil.getItemByAppName(con,item['app_name'])
#        if oldItem == []:
#            print "数据库中无该App记录，执行插入操作"
#        elif CommonUtil.cmpVersion(oldItem[0][5], item['version']): 
#            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
#        return item


#'''
#执行顺序ID：103
#数据库插入或者更新操作
#'''
#class DatebasePipeline(object):
#    def process_item(self,item,spider):
#        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
#        if SqliteUtil.getItemByAppName(con,item['app_name']) != []:
#            #更新数据
#            print "数据库更新数据"
#            sql = '''
#                UPDATE  app_info SET
#                    apk_url = ? ,
#                    pakage_name = ?,
#                    cover = ?,
#                    version = ?,
#                    rating_star = ?,
#                    rating_count = ?,
#                    category = ?,
#                    android_version = ?,
#                    download_times = ?,
#                    author = ?,
#                    last_update = ?,
#                    description = ?,
#                    imgs_url = ?,
#                    apk_size = ?,
#                    platform = ?
#                WHERE app_name = ? '''
#            data = [(
#                item['apk_url'],
#                item['pakage_name'],
#                item['cover'],
#                item['version'],
#                item['rating_star'],
#                item['rating_count'],
#                item['category'],
#                item['android_version'],
#                item['download_times'],
#                item['author'],
#                item['last_update'],
#                item['description'],
#                item['imgs_url'],
#                item['apk_size'],
#                item['platform'],
#                item['app_name'])]
#        else:
#            #插入数据
#            print '数据库插入数据'
#            sql = '''INSERT INTO app_info values(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
#            data = [(
#                    item['apk_url'],
#                    item['pakage_name'],
#                    item['app_name'],
#                    item['cover'],
#                    item['version'],
#                    item['rating_star'],
#                    item['rating_count'],
#                    item['category'],
#                    item['android_version'],
#                    item['download_times'],
#                    item['author'],
#                    item['last_update'],
#                    item['description'],
#                    item['imgs_url'],
#                    item['apk_size'],
#                    item['platform'])]
#                    
#        SqliteUtil.save_or_update(con, sql, data)
#        print '数据库操作结束'
#        return item