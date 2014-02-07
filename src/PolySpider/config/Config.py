#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


def get_base_path():
    '''
    ##获取当前环境根目录
    *   如果是通过scrapy crawl spider运行并访问该module，则在PATH中存在`系统目录/PolySpider/src`，我们只需要把该目录返回即可
    *   如果是通过web.py来访问该module,则并不保证该艮目存在，因此需要向path中添加该目录
    '''
    for p in sys.path:
        if 'PolySpider' in p and 'src' in p and not 'web' in p:
            return p
    c_path = os.getcwd()
    base_path = c_path[:c_path.rfind("src") + 3]
    sys.path.append(base_path)
    return base_path

REDIS = {
    'host':'localhost',
    'password':'',
    'port':6379,
    'db':0
}

# App Star Constant
APPSTAR_MAX_APPS = 3000

BAIDU_YUN = {
    '''
    这里需要填写BaiYun的公钥AK，私钥SK和Bucket
    '''
    'ak': '',
    'sk': '',
    'bucket': ''
}

UPYUN = {
    '''
    这里需要填写申请下来的又拍云所对应的bucket的用户名和密码
    '''
    'user_name': '',
    'password': '',
    'bucket': ''
}
