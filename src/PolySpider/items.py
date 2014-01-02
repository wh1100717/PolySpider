#!/usr/bin/env python
#coding:gbk

from scrapy.item import Item, Field

class AppItem(Item):
    """
    获取应用的具体信息：
    apk_url: apk下载链接
    pakage_name: 应用包名
    app_name: 应用名称
    cover: 封面图片url地址
    version: 版本号
    rating_star: 总评分
    rating_count: 评分总数
    category: 类别
    android_version: 支持的Android版本
    download_times: 下载次数
    author: 作者或公司
    last_update: 最后更新时间
    description: 应用简介
    imgs_url: 应用截图链接
    """
    app_url = Field()
    apk_url = Field()
    pakage_name = Field()
    app_name = Field()
    cover = Field()
    version = Field()
    rating_star = Field()
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
    
    def __repr__(self):
        #Debug和Info模式下，Pipeline处理完成后不打印Item内容
        return "\n"
    