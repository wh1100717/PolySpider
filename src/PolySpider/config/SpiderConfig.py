#!/usr/bin/env python
# -*- coding: utf-8 -*-  

'''
    #Intro
    *   Spider是通过xpath来定位要解析的内容的
    *   SpiderConfig将所有spider中用到的xpath分离出来统一管理。
'''
app_china = {
    'apk_url' :'//div[@class="down-box cf"]/a[3]/@href',
    'package_name' : '//*[@id="app_pkg"]/@value',
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

app_star = {
    'apk_url' :"//*[@id='appDetail']/li[1]/a/@href",
    'package_name' : '',
    'app_name' :'//*[@id="appName"]/text()',
    'cover' :'//*[@id="appImg"]/@src',
    'version' :'//*[@id="appVersion"]/text()',
    'rating_point' :'//*[@id="appDetail"]/li[1]/span/text()',
    'rating_count' :'//*[@id="appDetail"]/li[2]/span[1]/text()',
    'category' :'//*[@id="appDetail"]/li[1]/text()',
    'android_version' :'//*[@id="appDetail"]/li[1]/text()',
    'download_times' :'//*[@id="appDetail"]/li[2]/text()[2]',
    'author' :'//*[@id="appDetail"]/li[2]/text()[3]',
    'last_update' :'//*[@id="appDetail"]/li[2]/span[2]/text()',
    'description' :'//*[@id="appDes"]/p/text()',
    'apk_size' :'//*[@id="appDetail"]/li[1]/text()[3]',
    'imgs_url' :'//li/img/@src'
}
baidu = {
    'apk_url' :'//*[@id="down_as_durl"]/@href',
    'package_name' : "//*[@class='event-exe-install info-download']/@data-package",
    'app_name' :"//*[@id='appname']/text()",
    'cover' :"//*[@id='app-logo']/@src",
    'version' :'//div/table/tbody/tr/td/span[@class="params-vname"]/text()',
    'rating_point' :"//*[@id='score-num']/text()",
    'rating_count' :"//*[@id='score-participants']/text()",
    'category' :"//span[@class='params-catename']/text()",
    'android_version' :'//div/table/tbody/tr/td/span[@class="params-platform"]/text()',
    'download_times' :'//*[@class="params-download-num"]/text()',
    'author' :'',
    'last_update' :'//div/table/tbody/tr/td/span[@class="params-updatetime"]/text()',
    'description' :"//*[@class='brief-des']/text()",
    'apk_size' :'//div/table/tbody/tr/td/span[@class="params-size"]/text()',
    'imgs_url' :"//ul[@class='screen cls data-screenshots']/li/img/@src"
}
xiaomi = {
    'apk_url' :'/html/body/div[2]/div[1]/div[3]/div[1]/a/@href',
    'package_name' : '/html/body/div[2]/div[2]/ul[1]/li[4]/h4/text()',
    'app_name' :'/html/body/div[2]/div[1]/div[2]/h1/text()',
    'cover' :"/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/img/@src",
    'version' :'/html/body/div[2]/div[2]/ul[1]/li[2]/h4/text()',
    'rating_point' :'/html/body/div[2]/div[1]/div[3]/div[1]/div[2]/@class',
    'rating_count' :'',
    'category' :'/html/body/div[2]/div[2]/ul[1]/li[1]/h4/text()',
    'android_version' :'',
    'download_times' :'',
    'author' :'/html/body/div[2]/div[2]/ul[1]/li[6]/h4/text()',
    'last_update' :'/html/body/div[2]/div[2]/ul[1]/li[3]/h4/text()',
    'description' :'/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/p/text()',
    'apk_size' :'/html/body/div[2]/div[2]/ul[1]/li[5]/h4/text()',
    'imgs_url' :'//*[@id="J_thumbnail_wrap"]/img/@src'
}
hiapk = {
    'apk_url' :'//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href',
    'package_name' : '//head/script[15]/text()',
    'app_name' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()',
    'cover' :'//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src',
    'version' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()',
    'rating_point' :'//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/@class',
    'rating_count' :'//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()',
    'category' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()',
    'android_version' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()',
    'download_times' :'//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()',
    'author' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()',
    'last_update' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftPublishTime"]/text()',
    'description' :'//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()',
    'apk_size' :'//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSize"]/text()',
    'imgs_url' :'//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href'
}
google_play = {
    'apk_url' :'',
    'package_name' : "//*[@class='details-wrapper apps square-cover id-track-partial-impression']/@data-docid",
    'app_name' :'//*[@itemprop="name"]/div/text()',
    'cover' :'//div[@class="cover-container"]/img[@class="cover-image"]/@src',
    'version' :'//*[@itemprop="softwareVersion"]/text()',
    'rating_point' :'//*[@class="score"]/text()',
    'rating_count' :'//*[@class="reviews-num"]/text()',
    'category' :'//*[@itemprop="genre"]/text()',
    'android_version' :'//*[@itemprop="operatingSystems"]/text()',
    'download_times' :'//*[@itemprop="numDownloads"]/text()',
    'author' :'//span[@itemprop="name"]/text()',
    'last_update' :'//*[@itemprop="datePublished"]/text()',
    'description' :'//*[@class="id-app-orig-desc"]',
    'apk_size' :'//*[@itemprop="fileSize"]/text()',
    'imgs_url' :'//*[@class="thumbnails"]/img/@src'
}
gfan = {
    'apk_url' :'//*[@id="computerLoad"]/@href',
    'package_name' : "",
    'app_name' :'//*[@class="curr-tit"]/text()',
    'cover' :'//*[@class="app-view png"]/@src',
    'version' :'//*[@class="app-info"]/p[1]/text()',
    'rating_point' :'//*[@class="app-marking png"]/text()',
    'rating_count' :'//*[@class="marking-tips"]/text()',
    'category' :'//*[@class="curr-site"]/text()',
    'android_version' :'//*[@class="app-info"]/p[6]/text()',
    'download_times' :'',
    'author' :'//*[@class="app-info"]/p[2]/text()',
    'last_update' :'//*[@class="app-info"]/p[3]/text()',
    'description' :'//*[@class="app-intro"]/text()',
    'apk_size' :'//*[@class="app-info"]/p[4]/text()',
    'imgs_url' :'//*[@class="simg"]/@src'
}
muzhiwan = {
    'apk_url' :'//*[@class="local"]/@href',
    'package_name' : '//*[@name="package"]/@value',
    'app_name' :'//*[@class="game_name"]/h1/text()',
    'cover' :'//*[@class="game_icon"]/img/@src',
    'version' :'//*[@id="gameVersion"]/text()',
    'rating_point' :'',
    'rating_count' :'//*[@id="commentTitle"]/span/text()',
    'category' :'//*[@class="clear"]/ul/li[6]/a[contains(@href,"category")]/text()',
    'android_version' :'//*[@class="clear"]/ul/li[8]/text()',
    'download_times' :'//*[@class="clear"]/ul/li/span[@id="downCount"]/text()',
    'author' :'//*[@class="clear"]/ul/li/a[@rel="nofollow"]/text()',
    'last_update' :'//*[@class="clear"]/ul/li[5]/text()',
    'description' :'//*[@itemprop="description"]/text()',
    'apk_size' :'//*[@class="clear"]/ul/li[2]/text()',
    'imgs_url' :'//*[@itemprop="screenshot"]/@src'
}