#!/usr/bin/env python
#coding:gbk

from scrapy.item import Item, Field

class AppItem(Item):
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
