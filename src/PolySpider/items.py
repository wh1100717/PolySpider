#!/usr/bin/env python
#coding:gbk

from scrapy.item import Item, Field

class AppItem(Item):
    apk_url = Field()
    pakage_name = Field()
#    name = Field()
#    cover = Field()
#    detail_page = Field()
#    company = Field()
#    star_rating = Field()
#    price = Field()
#    href = Field()
#    subtitle = Field()
#    description = Field()
#    price = Field()
#    author = Field()
#    lastUpdate = Field()