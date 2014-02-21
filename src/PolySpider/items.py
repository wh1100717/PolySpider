#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from scrapy.item import Item, Field
'''
Scrapy抓取的Model类，用来定义抓取Item的数据内容和格式
Item会在Spider中进行抓取，然后在pipeline中进行数据处理和加工并最终存储到Redis中。
'''
class AppItem(Item):
    """
    获取应用的具体信息：
    apk_url: apk下载链接
    package_name: 应用包名
    app_name: 应用名称
    cover: 封面图片url地址
    version: 版本号
    rating_point: 总评分
    rating_count: 评分总数
    category: 类别
    android_version: 支持的Android版本
    download_times: 下载次数
    author: 作者或公司
    last_update: 最后更新时间
    description: 应用简介
    imgs_url: 应用截图链接
    apk_size: apk文件的大小
    platform: 抓取该应用的源，比如baidu，xiaomi等
    app_category: 用来临时存储获取的app的categroy

    DROP_APP： 标识符，用来存储该应用是否要丢弃
    NEW_APP: 标识符，用来存储该应用是否为新应用
    UPDATE_APP: 标识符，用来存储该应用是否为更新的应用
    """
    app_id = Field()
    apk_url = Field()
    package_name = Field()
    app_name = Field()
    cover = Field()
    version = Field()
    rating_point = Field()
    rating_count = Field()
    category = Field()
    android_version = Field()
    download_times = Field()
    author = Field()
    last_update = Field()
    description = Field()
    imgs_url = Field()
    apk_size = Field()
    platform = Field()
    
    app_category = Field()#用来临时存储获取的app的category
    DROP_APP = Field()
    NEW_APP = Field()
    UPDATE_APP = Field() 
    
    def __repr__(self):
        #Debug和Info模式下，Pipeline处理完成后不打印Item内容
        return "\n"
    