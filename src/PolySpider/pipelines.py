#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from scrapy.exceptions import DropItem
from PolySpider.util import CategoryUtil
from PolySpider.dao import AppDao
from PolySpider.dao import StatusDao

'''
#以下类库分别用于文件上传、下载、apk分析等方面的操作，目前已经完成，但是还不需要使用
import urllib
import pybcs
from PolySpider.util import ApkUtil
from PolySpider.util import FileUploadUtil
from PolySpider.util import CommonUtil
from PolySpider.config import Config
'''

# 关于pipeline对item数据的处理，专门撰写了一个文档进行描述，包含了详细的流程图和处理过程


class PolySpiderPipeline(object):

    def process_item(self, item, spider):
        return item


class CategorizingPipeline(object):

    '''
    执行顺序ID：100
    处理应用的分类的Pipeline~
    '''

    def process_item(self, item, spider):
        # 判断item是否为空，如果为空，则drop item
        if not item or not item['app_name']:
            raise DropItem(item)
        # 如果category中没有这个类 会报错
        item['category'] = CategoryUtil.get_category_id_by_name(
            item['category'].encode('utf8', 'ignore'),item)
        item['DROP_APP'] = False
        item['NEW_APP'] = False
        item['UPDATE_APP'] = False
        return item


class CheckAppPipeline(object):

    '''
    执行顺序ID：101
    检查app中是否存在该App数据
    如果不存在，则记录该App数据
    如果存在，检查author,如果为空，则更新author
    '''

    def process_item(self, item, spider):
        app = AppDao.get_app_by_app_name(item['app_name'])
        if not app:
            # 构造分类
            temp = ""
            for category in item['category'].split(","):
                temp = temp + category + ":1,"
            item['category'] = temp[:-1]
            # 插入数据
            item['app_id'] = AppDao.insert_app(item)
            item['NEW_APP'] = True
        else:
            item['app_id'] = app['app_id']
            item['app_category'] = app['category']
            # 判断author是否为空，如果为空，则更新app表
            if app['author'] == "" and item['author'] != "":
                AppDao.update_app_author(app['app_id'], item['author'])
            # 判断package_name是否为空，如果为空，则更新app表
            if app['package_name'] == "" and item['package_name'] != "":
                AppDao.update_app_packagename(app['app_id'], item['package_name'])
        return item


class CheckAppDetailsPipeline(object):

    '''
    执行顺序ID：102
    分析ps_app_detail表中是否存在该App_Detail数据(通过app_id, verison, flatform做唯一标识)
    如果不存在，则记录该App数据
    如果存在，更新一些数据信息，然后将该ItemDrop掉
    '''

    def process_item(self, item, spider):
        app_detail_list = AppDao.get_app_detail_by_app_name(item['app_name'])
        if app_detail_list == None:
            item['DROP_APP'] = True
            return item
        for app_detail in app_detail_list:
            if str(app_detail['version']) == item['version'] and app_detail['platform'] == item['platform']:
                item['DROP_APP'] = True
                print 'DROP THIS ITEM %s' %item['app_name']
                break
        else:
            if not item['pakage_name']:
                self.apk_operation(item)
            print 'INSERT APP DETAIL %s' %item['app_name']
            AppDao.insert_app_detail(item)
        return item

    def apk_operation(self, item):
        '''
        执行顺序ID：102
        文件上传到服务器
        分析Apk信息,获取pakage_name
        上传到UpYun/BaiduYun
        '''
        '''暂时不需要apk下载及分析流程(功能已实现并测试)
        url = item['apk_url']
        ##根据获取的apk下载地址将apk文件传至百度云
        #正则匹配文件名
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #下载文件至本地
        print 'Download apk file locally： %s ' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        #开始下载
        #调用进度条，传入下载url和文件名称
        CommonUtil.progressbar(url,'apk/' + name)
        print 'Download finish'
        #下载文件至本地 Done
        
        #分析APK文件，获取里面的info_list
        #目前值获取了里面的pakage_name，以后可以增加别的需要的属性
        print 'Start parsing apk file'
        info_list = ApkUtil.getInfoList(name)
        item['pakage_name'] = info_list['packageInfo']['orig_package']
        print 'parsing finish'
        '''
        item['pakage_name'] = ''
        # Done
        return True

        '''
        #上传至百度云
        bcs = pybcs.BCS('http://bcs.duapp.com/', Config.BAIDU_AK, Config.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(Config.BAIDU_BUCKET)
        #声明一个object
        print 'Start upload apk %s to BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        print "%s\n%s\n%s\n%s\n" %(Config.BAIDU_AK,Config.BAIDU_SK,Config.BAIDU_BUCKET,name)
        obj.put_file('apk/' + name)
        #上传至百度云 Done

        #上传至UpYun
        print 'Start upload apk %s to UpYun' %name
        up = FileUploadUtil.UpYun()
        up.put('apk/' + name, 'apk/' + name)
        #上传至UpYun Done
        print 'Upload Finish'
        '''


class UpdateCategoryPipeline(object):

    '''
    执行顺序ID：103
    更新ps_app中的category项
    '''

    def process_item(self, item, spider):

        if item['DROP_APP']:
            return item
        if not item['NEW_APP']:
            item['UPDATE_APP'] = True
            # 重新计算category
            item_category_ids = item['category'].split(",")
            categories = item['app_category'].split(",")
            for item_category_id in item_category_ids:
                flag = True
                for index in range(len(categories)):
                    category = categories[index]  # 2200:1
                    app_category_id = category[:category.find(":")]  # 2200
                    if app_category_id == item_category_id:
                        categories[index] = app_category_id + ":" + str(
                            int(category[(category.find(":") + 1):]) + 1)
                        flag = False
                        break
                if flag:
                    categories.append(item_category_id + ":1")
            item['app_category'] = ",".join(self.category_reorder(categories))

            # 更新app的category
            AppDao.update_app_category(item['app_id'], item['app_category'])
        return item

    def category_reorder(self, categories):
        length = len(categories)
        for i in range(length - 1):
            for j in range(length - i - 1):
                order_category = categories[j]
                order_category_value = int(
                    order_category[(order_category.find(":") + 1):])
                cmp_category = categories[j + 1]
                cmp_category_value = int(
                    cmp_category[(cmp_category.find(":") + 1):])
                if cmp_category_value > order_category_value:
                    categories[i], categories[
                        i + 1] = categories[i + 1], categories[i]
        return categories


class StatusRecordPipeline(object):

    '''
    执行顺序ID：104
    更新Status
    '''

    def process_item(self, item, spider):
        StatusDao.status_incr(item['platform'], 'crawled')
        if item['NEW_APP']:
            StatusDao.status_incr(item['platform'], 'new')
        if item['UPDATE_APP']:
            StatusDao.status_incr(item['platform'], 'update')
        return item