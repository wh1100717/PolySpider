#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from PolySpider.util import RedisUtil

redis_client = RedisUtil.RedisClient()

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
'''


def get_today_status_by_platform(platform):
    today = str(datetime.date.today())
    data = redis_client.hget_all('status::' + today + '&' + platform)
    if not data:
        yesterday = str(today - datetime.timedelta(days = 1))
        if redis_client.exists('status::' + yesterday + '&' + platform):
            #TODO 增加对于历史status数据的处理流程
            pass
        data = {'crawled': 0, 'new': 0, 'update': 0}
        redis_client.hset_map('status::' + today + '&' + platform, data)
    return data

def status_incr(platform, map_key):
    today = str(datetime.date.today())
    redis_client.hincr('status::' + today + '&' + platform, map_key)
