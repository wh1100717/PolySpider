#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PolySpider.util import RedisUtil

redis_client = RedisUtil.RedisClient()

'''
app::index:
	存储格式为key-map_key-value
		key --> app_index
		map_key --> app_name
		value --> app_id
app::(id):
	存储格式为key-map_key-value
		key --> app::(id)
		map_key --> app_id | app_name | author | category | app_detail
		value --> 举例： 0 | '微信' | '腾讯' | '2001:1' | [{},{},...]
    Note: map_key --> detail中存放的是app的细节信息，以数组的项来存储，每一项以哈希的形式存储
'''


def get_app_by_app_name(app_name):
    '''
    ##根据app_name来获取app record
    *   input: app_name
    *   output: app(dictionary)
    '''
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    if not app_id:
        return None
    else:
        tmp=eval(redis_client.get_items('app',app_id,app_id)[0])
        tmp['app_id']=app_id
        return tmp


def get_app_detail_by_app_name(app_name):
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    print 'app_id : %s' %app_id
    if not app_id:
        return None
    else:
        tmp=eval(redis_client.get_items('app',app_id,app_id)[0])
        app_detail=tmp.get('app_detail')
        return app_detail if app_detail else []


def insert_app(item):
    app_id = redis_client.incr('app_id')
    print "app_id : %d" % app_id
    while redis_client.get_length('app')<=app_id:
        redis_client.rpush('app',0)
    else:
        tmp={'app_name':item['app_name'],'author':item['author'], 'category':item['category']}
        print tmp
        print redis_client.get_length('app')
        redis_client.lset('app',app_id,tmp)
        
    print redis_client.hset('app::index', item['app_name'], app_id)
    #print redis_client.hset('app::' + str(app_id), app_id=app_id, app_name=item['app_name'], author=item['author'], category=item['category'])
    return app_id


def insert_app_detail(item):
    '''
    version | platform | apk_url | apk_size | pakage_name | cover | rating_point | rating_count | android_version |
    download_times | description | imgs_url | last_update
    '''
    app_detail_map = {
        'version': item['version'],
        'platform': item['platform'],
        'apk_url': item['apk_url'],
        'apk_size': item['apk_size'],
        'pakage_name': item['pakage_name'],
        'cover': item['cover'],
        'rating_point': item['rating_point'],
        'rating_count': item['rating_count'],
        'android_version': item['android_version'],
        'download_times': item['download_times'],
        'description': item['description'],
        'imgs_url': item['imgs_url'],
        'last_update': item['last_update']
    }
    #app_detail = redis_client.hget('app::' + str(item['app_id']), 'app_detail')
    tmp=eval(redis_client.get_items('app',item['app_id'],item['app_id'])[0])
    tmp=dict(tmp,**app_detail_map)
#    if app_detail:
#        app_detail.append(app_detail_map)
#    else:
#        app_detail = [app_detail_map]
#    redis_client.hset('app::' + str(item['app_id']), app_detail=app_detail)
    print redis_client.set_item('app',item['app_id'],tmp)

def update_app_author(app_id, author):
    '''
    ##更新app中的作者信息
    *   input: id | author
    '''
    #print redis_client.hset('app::' + str(app_id), author=author)
    
    tmp=eval(redis_client.get_items('app',app_id,app_id)[0])
    tmp['author']=author
    print redis_client.set_item('app',app_id,tmp)
    

def update_app_category(app_id, category):
    '''
    ##更新app中的分类信息
    *   input: id | category
    '''
    tmp=eval(redis_client.get_items('app',app_id,app_id)[0])
    tmp['category']=category
    print redis_client.set_item('app',app_id,tmp)


def update_app_detail(app_id, app_detail):
    print redis_client.hset('app::' + str(app_id), app_detail=app_detail)
