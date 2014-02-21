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

'''
    #REDIS配置地址
    *   host: 填写Redis服务器名称或者IP
    *   password: 添加Redis服务器的密码，默认为空
    *   port: 服务器端口，默认为6379
    *   db: redis中配置的数据库编号，默认为0
'''
REDIS = {
    'host':'localhost',
    'password':'',
    'port':6379,
    'db':0
}

'''
    ##Tor+polipo
    ###安装polipo步骤：
    *   1. `git clone git://git.wifi.pps.univ-paris-diderot.fr/polipo` 下载最新源码
    *   2. 执行`make all`
            >可能会报错，说`makeinfo命令未找到`，需要安装依赖库`yum install texinfo`
    *   3. 执行`su -c 'make install'`
    *   4. 利用`man polipo`查看命令帮助
    *   5. 执行`polipo &` 启动polipo
    HTTP_PROXY为polipo端口，在polipo的/etc/polipo/config文件配置Tor端口`socksParentProxy = localhost:9050`
    在Util中添加TorUtil
    在Setting中的DOWNLOADER_MIDDLEWARES添加TorUtil下的ProxyMiddleware
    在服务器启动Tor和polipo服务
    由于国内对Tor墙掉了 导致这一部分无法进行 所以暂时搁置
    
'''
HTTP_PROXY = 'http://127.0.0.1:8123'

'''
    ##Spider配置信息
    *   appstar和xiaomi的应用详细页都是按照数字排序的，所以他们的spider实际上不需要爬，只需要根据顺序来依次访问页面获取应用数据即可
'''
# App Star Constant
APPSTAR_MAX_APPS = 3000
XIAOMI_MAX_APPS = 56000

'''
    ##云存储配置信息
    *   利用baidu_yun的接口实现了apk上传功能
    *   重新了upyun得接口实现了带进度条、下载速度、完成时间预估等特性的apk上传功能
'''
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
