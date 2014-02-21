#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PolySpider.util import RedisUtil
'''
    app::amount:
        用来实现app_id的auto_increasement功能
    app::index:
        用来做app_name和app_id的键值对应
        存储格式为key-map_key-value   --> hash
            key --> app::index
            map_key --> app_name
            value --> app_id
    app::data:
        用来存储app的数据
        存储格式为key-index-value   --> list
            key --> app::data
            map_key --> app_id 
            value --> 举例： 'app_id':0,'app_name':'QQ','author':'Tencent','category':'社交','app_detail':[{},{}]
    app::category:
        用来存储分类数据
        存储格式为key-map_key-value   --> hash
            key --> app::category
            map_key --> category_id
            value --> 包含了属于该分类下app_id的集合，类型为set
    app::platform:
        用来存储平台数据
        存储格式为key-map_key-value   --> hash
            key --> app::platform
            map_key --> platform_name
            value --> 包含了属于该平台下的分类app_id的集合，类型为set
'''


'''
    ##初始化Redis
    *   Redis的具体操作封装在了RedisUtil中
    *   所有的redis操作利用redis_client来实现
'''
redis_client = RedisUtil.RedisClient()


def get_app_by_app_id(app_id):
    '''
    ##根据app_id来获取app record
    *   redis_client.get_item()返回的是字符串，需要转换成object，故用eval()函数来实现
    '''
    return eval(redis_client.get_item('app::data',app_id)) if app_id else None

def get_app_detail_by_app_name(app_name):
    '''
    ##根据app_name来获取app_detail
    *   app_detail为app中的一个属性，存储着app得详细数据，类型为list,每一个item中存放着相应平台和版本的具体app详情
    '''
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    return get_app_by_app_id(app_id)['app_detail']


def get_app_by_app_name(app_name):
    '''
    ##根据app_name来获取app record
    *   input: app_name
    *   output: app::data()
    '''
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    return get_app_by_app_id(app_id)


def insert_app(item):
    '''
    ##向app::data中插入新的app数据
    '''
    #通过app::amount来实现类似sql中的autoincrease功能
    app_id = redis_client.incr('app::amount')
    while redis_client.get_length('app::data')<=app_id:
        redis_client.push_items('app::data',0)
    else:
        #创建一个新的app字典
        new_app = {
            'app_id': app_id,
            'app_name':item['app_name'],
            'author':item['author'],
            'category':item['category'],
            'package_name': item['package_name'],
            'app_detail':[]
            }
        #插入到app::data中的app_id位置
        redis_client.set_item('app::data',app_id,new_app)
    #处理分类
    #当app执行插入操作，则说明是一个全新的app，那么需要在`app::category`中进行记录
    '''
    在redis中单独建立了一个数据结构用来管理分类情况，类似于数据库中的索引，但有所区别
    可以利用`app::category`快速定位该分类下得数据，不需要对整个`app::data`进行搜索
    '''
    #TODO 目前阶段是直接讲redis得操作过程放在函数里实现，耦合度过高
    #在PolySpider v0.5中需要将所有持久化层的操作抽离出来，利用接口的方式进行实现
    new_categories=item['category'].split(',')
    for new_category in new_categories:
        category_set= redis_client.hget('app::category',str(new_category.split(':')[0]))
        if category_set:
            category_set=eval(category_set)
            category_set.add(app_id)
            redis_client.hset('app::category',str(new_category.split(':')[0]),category_set)
        else:
            redis_client.hset('app::category',str(new_category.split(':')[0]),set([app_id]))
    redis_client.hset('app::index', item['app_name'], app_id)
    return app_id


def insert_app_detail(item):
    '''
    ##插入app的详细信息
        app_detail中包含了app的详细信息，具体信息如下：
            *   version: 版本号
            *   platform: 平台(表示是从哪个平台抓取来的数据，例如xiaomi, googleplay等)
            *   apk_url: 抓取来的apk的下载地址
            *   apk_size: apk的大小
            *   cover: 封面图片的地址
            *   rating_point: 该应用的评分
            *   rating_count: 该应用的评论数
            *   android_version: 该应用支持的android版本
            *   download_times: 下载次数
            *   description: 该应用的介绍
            *   imgs_url: 介绍该应用展示的图片(因为图片一般是多张的，所以实际存储的是以空格分隔的url字符串，可以直接利用split()转换成url数组)
            *   last_update: 该应用的更新日期
        从不同平台抓取来的应用，包括版本、apk大小，介绍等信息都可能不一样，所以为了区分，我们设置app_detail为list格式，
        每一个平台所对应的一个版本的app理解成队里app_detail中的一个item
        那么insert_app_detail操作实际上就是对这个list进行append item操作
    '''
    app_detail_map = {
        'version': item['version'],
        'platform': item['platform'],
        'apk_url': item['apk_url'],
        'apk_size': item['apk_size'],
        'cover': item['cover'],
        'rating_point': item['rating_point'],
        'rating_count': item['rating_count'],
        'android_version': item['android_version'],
        'download_times': item['download_times'],
        'description': item['description'],
        'imgs_url': item['imgs_url'],
        'last_update': item['last_update']
    }
    app = redis_client.get_item('app::data', item['app_id'])
    if app:
        app = eval(app)
    else:
        return False
    app['app_detail'].append(app_detail_map)
    redis_client.set_item('app::data',item['app_id'],app)
    app_platform= redis_client.hget('app::platform',item['platform'])
    if app_platform:
        app_platform=eval(app_platform)
        app_platform.add(item['app_id'])
        redis_client.hset('app::platform',item['platform'],app_platform)
    else:
        redis_client.hset('app::platform',item['platform'],set([item['app_id']]))
    return True

       

def update_app_author(app_id, author):
    '''
    ##更新app中的作者信息
    *   有的平台中没有author信息，所以当获取到author信息以后添加到app的数据中，保证数据完整性
    *   input: id | author
    '''
    new_app=redis_client.get_item('app::data',app_id)
    if new_app:
        new_app = eval(new_app)
    else:
        return False
    new_app['author']=author
    redis_client.set_item('app::data',app_id,new_app)
    return True
    

def update_app_category(app_id, category):
    '''
    ##更新app中的分类信息
    *   首先更新`app::data`中的`category`信息
    *   其次更新`app::category`中存储的app信息.
    *       比如说应用`QQ`原本是`通讯`分类，现在要更改为`社交`分类
    *       那么除了更改`app::data`中QQ的`category`属性为`社交`以外，
    *       还需要将`app::category`中`通讯`下的`QQ`移除，并在`社交`中添加`QQ`
    '''
    new_app=redis_client.get_item('app::data',app_id)
    if new_app:
        new_app = eval(new_app)
    else:
        return False
    new_app['category']=category
    new_categorys=category.split(',')
    for i in range(len(new_categorys)):
        if i==0:
            category_set= redis_client.hget('app::category',int(new_categorys[i].split(':')[0]))
            if category_set:
                category_set=eval(category_set)
                category_set.add(app_id)
                redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),category_set)
            else:
                redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),set([app_id]))
        else:
            category_set= redis_client.hget('app::category',int(new_categorys[i].split(':')[0]))
            if category_set:
                category_set=eval(category_set)
                if app_id in category_set:
                    category_set.remove(app_id)
                    redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),category_set)
    redis_client.set_item('app::data',app_id,new_app)
    return True

