#!/usr/bin/env python
# -*- coding: utf-8 -*-  

#app_china spider xpath configuration
app_china = {
    'apk_url' :'//div[@class="down-box cf"]/a[3]/@href',
    'pakage_name' : '//*[@id="app_pkg"]/@value',
    'app_name' :'//h1[@class="ch-name cutoff fl"]/text()',
    'cover' :'//div[@class="cf"]/img/@src',
    'version' :'//*[@id="app-detail-wrap"]/div[2]/div[2]/p[1]/text()',
    'rating_point' :'',
    'rating_count' :'//a[@class="linkmore"]/text()',
    'category' :'//*[@id="app-detail-wrap"]/div[2]/ul/li[3]/a/text()',
    'android_version' :'//*[@id="app-detail-wrap"]/div[1]/span[@class="sys"]/text()',
    'download_times' :'//*[@id="app-detail-wrap"]/div[2]/ul/li[2]/em/text()',
    'author' :'//span[@class="dl authon-name"]/text()',
    'last_update' :'//*[@id="app-detail-wrap"]/div[2]/ul/li[4]/text()',
    'description' :'//*[@id="scrollbar1"]/div[2]/div/div/text()',
    'apk_size' :'//*[@id="app-detail-wrap"]/div[2]/ul/li[1]/text()',
    'imgs_url' :'//*[@id="makeMeScrollable"]/a/@href'
}

