#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PolySpider.util import RedisUtil

redis_client = RedisUtil.RedisClient()

'''
app::index:
	存储格式为key-map_key-value
		key --> app::index
		map_key --> app_name
		value --> app_id
app::data:
	存储格式为key-index-value
		key --> app::data
		map_key --> app_id 
		value --> 举例： 'app_id':0,'app_name':'QQ','author':'Tencent','category':'社交','app_detail':[{},{}]
   
'''

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
    version | platform | apk_url | apk_size |  cover | rating_point | rating_count | android_version |
    download_times | description | imgs_url | last_update
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
    app = eval(redis_client.get_item('app::data', item['app_id']))
    if app:
        app['app_detail'].append(app_detail_map)
        print redis_client.set_item('app::data',item['app_id'],app)
        app_platform= redis_client.hget('app::platform',item['platform'])
        if app_platform:
            app_platform=eval(app_platform)
            app_platform.add(item['app_id'])
            redis_client.hset('app::platform',item['platform'],app_platform)
        else:
            redis_client.hset('app::platform',item['platform'],set([item['app_id']]))
       

def update_app_author(app_id, author):
    '''
    ##更新app中的作者信息
    *   input: id | author
    '''
    #print redis_client.hset('app::' + str(app_id), author=author)
    
    new_app=eval(redis_client.get_item('app::data',app_id))
    new_app['author']=author
    print redis_client.set_item('app::data',app_id,new_app)
    

def update_app_category(app_id, category):
    '''
    ##更新app中的分类信息
    *   input: id | category
    '''
    new_app=eval(redis_client.get_item('app::data',app_id))
    new_app['category']=category
    new_categorys=category.split(',')
    for new_category in new_categorys:
        category_set= redis_client.hget('app::category',str(new_category.split(':')[0]))
        category_set=eval(category_set)
        category_set.add(app_id)
        redis_client.hset('app::category',str(new_category.split(':')[0]),category_set)
    print redis_client.set_item('app::data',app_id,new_app)
