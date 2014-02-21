#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from PolySpider.util import RedisUtil
'''
status::(date):
    存储格式为key-map_key-value
    key --> status::(date&platform)
    map_key --> crawled, new, update
    value --> 0, 0, 0
status::history:
    存储除了当天以外的所有爬虫状态历史数据
    存储格式为key-map_key-value
    key --> status::history
    map_key --> date
    value -->   {
                platform1:{
                    crawled:0,
                    new:0,
                    update:0s
                    },
                platform2:{
                    crawled:0,
                    new:0,
                    update:0
                    }
                }
Note: 之所以把status::(data)和status::history分开，是因为status::history的存储结构导致不能实现具体某一个日期下某一个平台的数据自增功能
举例说明，A服务器上的SpiderA抓取了platform1上的一个应用，那么需要对crawled进行+1操作，流程为取出目前存储的crawled数据，执行+1操作，再update redis中的crawled数据
同时，B服务器中的SpiderB也抓取了platform1上得一个应用，如果在SpiderA update前，SpiderB就取出了crawled数据，那么最终的crawled结果不是crawled+2，而是crawled+1
因此少统计了一次数据的抓取。
为了解决这个问题，redis提供了incr操作，直接在data store端进行自+1操作，从而避免了数据的不准确性。
而incr操作只支持value元数据，因此需要对当天的status单独处理，
'''

'''
    ##初始化Redis
    *   Redis的具体操作封装在了RedisUtil中
    *   所有的redis操作利用redis_client来实现
'''
redis_client = RedisUtil.RedisClient()

def move_status_into_history(date, platform):
    '''
    ##将`status::(date&platform)`移入`status::history`
    *   在`status::history`中添加对应date和platform的数据
    *   将原本`status::(date&platform)`数据删除
    '''
    date = str(date) #输入的date可以是str格式，也可是datetime.date格式,这里会统一格式化为字符串
    data = redis_client.hget_all('status::' + date + '&' + platform)
    if redis_client.exists('status::history'):
        value = redis_client.hget('status::history', date)
        if value:
            value=eval(value)
            value[platform] = data
            redis_client.hset('status::history', date, value)
        else:
            redis_client.hset('status::history', date, {platform:data})
    else:
        redis_client.hset('status::history', date, {platform:data})
    redis_client.delete('status::' + date + '&' + platform)


def get_today_status_by_platform(platform):
    '''
    ##根据flatform来获取当天的状态数据
    *   这里会对昨天的status数据做检查，如果还存在昨天的status数据，则移入到`status::history`中
    '''
    today = str(datetime.date.today())
    data = redis_client.hget_all('status::' + today + '&' + platform)
    if not data:
        #TODO 目前是每更新一次status数据都要对昨天的历史数据做检查，也就是说要对访问一次redis，需要提供更好的方案
        yesterday = str(datetime.date.today() - datetime.timedelta(days = 1))
        if redis_client.exists('status::' + yesterday + '&' + platform):
            move_status_into_history(yesterday, platform)
        data = {'crawled': 0, 'new': 0, 'update': 0}
        redis_client.hset_map('status::' + today + '&' + platform, data)
    return data

def status_incr(platform, map_key):
    '''
    ##status中的数据执行自增操作
    '''
    get_today_status_by_platform(platform)
    today = str(datetime.date.today())
    redis_client.hincr('status::' + today + '&' + platform, map_key)
