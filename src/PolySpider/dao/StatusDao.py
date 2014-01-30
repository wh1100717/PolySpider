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
'''


def get_today_status_by_platform(platform):
    today = str(datetime.date.today())
    data = redis_client.hget_all('status::' + today + '&' + platform)
    if not data:
        data = {'crawled': 0, 'new': 0, 'update': 0}
        redis_client.hset_map('status::' + today + '&' + platform, data)
    return data

def status_incr(platform, map_key):
    today = str(datetime.date.today())
    redis_client.hincr('status::' + today + '&' + platform, map_key)
