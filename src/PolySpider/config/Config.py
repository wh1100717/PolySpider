#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os
import sys

def get_base_path():
    '''
    如果有则说明是在scrapy环境下
    如果没有说明是在web.py环境下
    '''
    for p in sys.path:
        if 'PolySpider' in p and 'src' in p and not 'web' in p:
            return p
    c_path = os.getcwd()
    base_path = c_path[:c_path.rfind("src")+3]
    sys.path.append(base_path)
    return base_path

def get_sqlite_path():
    if "win" in sys.platform:
        return get_base_path() + "\\" + "app.db"
    else:
        return get_base_path() + "/" + "app.db"

SHOW_SQL = False #True则会在控制台显示详细的SQL查询

#App Star Constant
APPSTAR_MAX_APPS = 3000

#BaiduYun AK && SK
'''这里需要填写BaiYun的公钥AK，私钥SK和Bucket'''
BAIDU_AK = ''
BAIDU_SK = ''
BAIDU_BUCKET = ''

#UpYun
'''这里需要填写申请下来的又拍云所对应的bucket的用户名和密码'''
UPYUN_USERNAME = ''
UPYUN_PASSWORD = ''
UPYUN_BUCKET = ''