#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import sys
import web
import os


reload(sys)
sys.setdefaultencoding('utf8')
c_path = os.getcwd()
sys.path.append(c_path[:c_path.rfind("src")+3])

from PolySpider.sql import App
from PolySpider.sql import AppDetail
from PolySpider.sql import Status
from PolySpider.util import StringUtil
from PolySpider.util import CategoryUtil
from view import render

render = web.template.render('templates/', base='layout')
render_without_layout = web.template.render('templates/')

urls = (
    '/(home/?)?', 'home',
    '/status/?', 'status',
    '/chart/?', 'chart',
    '/data/?', 'data',
    '/app/get_category_chart/?', 'get_category_chart',
    '/app/get_platform_chart/?','get_platform_chart',
    '/app/get_platform_chart_unique/?','get_platform_chart_unique',
    '/status/get_status_list/?','get_status_list',    
    '/status/get_status_list_by_platform/(.+)','get_status_list_by_platform',
    '/status/get_current_status_by_platform/(.+)','get_current_status_by_platform',
    '/status/get_current_status/','get_current_status',

)

class home:
    def GET(self,name):
        return render.home()

class status:
    def GET(self):
        return render.status()

class chart:
    def GET(self):
        return render.chart()

class data:
    def GET(self):
        apps = App.get_app_list()
        for index in range(len(apps)):
            data = list(apps[index])
            data[3]=CategoryUtil.get_category_name_by_id(data[3][0:4])
            apps[index]=tuple(data)
        app_details=AppDetail.get_app_detail_list()
        for index in range(len(app_details)):
            data = list(app_details[index])
            data[3]=CategoryUtil.get_category_name_by_id(data[3][0:4])
            app_details[index]=tuple(data)
        data=[apps,app_details]
        return render.data(data)

class get_category_chart:
    def GET(self):
        data  = App.get_app_categories()
        count_categorys={}
        count_categorys['1000']=0
        for category in data:
            for temp in category[0].split(','):
                app_category = temp.split(':')[0]
                if temp:
                    if app_category!='':
                        if not count_categorys.get(app_category):
                            count_categorys[app_category]=1
                        else:
                            count_categorys[app_category]=int(count_categorys[app_category])+1
                    else:
                        count_categorys['1000']=count_categorys['1000']
        data="["
        for count_category in count_categorys:
            data=data+'["'+unicode(str(CategoryUtil.get_category_name_by_id(count_category)))+'",'+str(count_categorys[count_category])+"],"
        data=data[:-1]+"]"
        return data

class get_platform_chart:
    def GET(self):
        data = AppDetail.get_platform_app_count()
        data =StringUtil.item_to_json(data)
        return data

class get_platform_chart_unique:
    def GET(self):
        data = AppDetail.get_platform_app_count_unique()
        data = StringUtil.item_to_json(data)
        return data

class get_status_list:
    def GET(self):
        data = StringUtil.item_to_json(Status.get_status_list())
        return data

class get_status_list_by_platform:
    def GET(self, platform):
#        data = StringUtil.item_to_json(Status.get_status_list_by_platform(platform))
#        data = '[[3,"xiaomi","2014-01-07",85,0,0],[5,"xiaomi","2014-01-08",100,15,17],[10,"xiaomi","2014-01-09",115,235,64],[10,"xiaomi","2014-01-10",125,343,132],[10,"xiaomi","2014-01-11",135,253,523],[10,"xiaomi","2014-01-12",145,546,654],[10,"xiaomi","2014-01-13",135,324,313],[10,"xiaomi","2014-01-14",165,231,653],[10,"xiaomi","2014-01-15",185,165,756],[10,"xiaomi","2014-01-16",125,111,432],[10,"xiaomi","2014-01-17",115,753,422],[10,"xiaomi","2014-01-18",145,234,814],[10,"xiaomi","2014-01-19",215,523,257],[10,"xiaomi","2014-01-20",245,423,857],[10,"xiaomi","2014-01-21",535,234,147],[10,"xiaomi","2014-01-22",645,132,457],[10,"xiaomi","2014-01-23",345,564,167]]'
#       data = '[[3,"xiaomi","2014-01-07",85,0,0],[5,"xiaomi","2014-01-08",100,15,17],[10,"xiaomi","2014-01-09",115,235,64],[10,"xiaomi","2014-01-10",125,343,132],[10,"xiaomi","2014-01-11",135,253,523],[10,"xiaomi","2014-01-12",145,546,654],[10,"xiaomi","2014-01-13",135,324,313],[10,"xiaomi","2014-01-14",165,231,653],[10,"xiaomi","2014-01-15",185,165,756],[10,"xiaomi","2014-01-16",125,111,432],[10,"xiaomi","2014-01-17",115,753,422],[10,"xiaomi","2014-01-18",145,234,814],[10,"xiaomi","2014-01-19",215,523,257],[10,"xiaomi","2014-01-20",245,423,857],[10,"xiaomi","2014-01-21",535,234,147],[10,"xiaomi","2014-01-22",645,132,457],[10,"xiaomi","2014-01-23",345,564,167],[3,"baidu","2014-01-07",160,381,117],[5,"baidu","2014-01-08",318,755,963],[10,"baidu","2014-01-09",333,648,290],[10,"baidu","2014-01-10",399,190,761],10,"baidu","2014-01-11",843,954,671],[10,"baidu","2014-01-12",383,772,498],[10,"baidu","2014-01-13",880,180,452],[10,"baidu","2014-01-14",120,431,627],[10,"baidu","2014-01-15",754,605,615],[10,"baidu","2014-01-16",450,905,421],[10,"baidu","2014-01-17",707,482,614],[10,"baidu","2014-01-18",787,225,926],[10,"baidu","2014-01-19",631,546,409],[10,"baidu","2014-01-20",185,814,633],[10,"baidu","2014-01-21",736,483,513],[10,"baidu","2014-01-22",248,400,267],[10,"baidu","2014-01-23",530,580,992],[3,"hiapk","2014-01-07",926,175,403],[5,"hiapk","2014-01-08",257,670,208],[10,"hiapk","2014-01-09",849,666,398],[10,"hiapk","2014-01-10",506,954,212],[10,"hiapk","2014-01-11",317,388,185],[10,"hiapk","2014-01-12",816,857,256],[10,"hiapk","2014-01-13",275,479,834],[10,"hiapk","2014-01-14",159,255,527],[10,"hiapk","2014-01-15",198,581,846],[10,"hiapk","2014-01-16",249,194,751],[10,"hiapk","2014-01-17",679,405,615],[10,"hiapk","2014-01-18",116,254,619],[10,"hiapk","2014-01-19",983,319,909],[10,"hiapk","2014-01-20",504,663,140],[10,"hiapk","2014-01-21",301,773,666],[10,"hiapk","2014-01-22",109,580,276],[10,"hiapk","2014-01-23",974,892,396],[3,"appstar","2014-01-07",564,999,657],[5,"appstar","2014-01-08",439,326,879],[10,"appstar","2014-01-09",659,529,948],[10,"appstar","2014-01-10",247,131,225],[10,"appstar","2014-01-11",445,806,685],[10,"appstar","2014-01-12",969,568,544],[10,"appstar","2014-01-13",351,906,657],[10,"appstar","2014-01-14",573,495,570],[10,"appstar","2014-01-15",677,810,887],[10,"appstar","2014-01-16",409,359,124],[10,"appstar","2014-01-17",956,576,669],[10,"appstar","2014-01-18",560,607,377],[10,"appstar","2014-01-19",755,396,611],[10,"appstar","2014-01-20",782,456,843],[10,"appstar","2014-01-21",985,493,930],[10,"appstar","2014-01-22",319,244,592],[10,"appstar","2014-01-23",968,532,903],[3,"appchina","2014-01-07",168,351,207],[5,"appchina","2014-01-08",248,999,694],[10,"appchina","2014-01-09",933,648,375],[10,"appchina","2014-01-10",369,334,888],[10,"appchina","2014-01-11",224,453,796],[10,"appchina","2014-01-12",797,911,879],[10,"appchina","2014-01-13",417,487,527],[10,"appchina","2014-01-14",364,892,135],[10,"appchina","2014-01-15",507,789,608],[10,"appchina","2014-01-16",151,559,271],[10,"appchina","2014-01-17",514,976,140],[10,"appchina","2014-01-18",848,688,936],[10,"appchina","2014-01-19",136,601,679],[10,"appchina","2014-01-20",154,104,237],[10,"appchina","2014-01-21",362,841,641],[10,"appchina","2014-01-22",179,313,396],[10,"appchina","2014-01-23",330,358,383]]'
        return data

class get_current_status_by_platform:
    def GET(self,platform):
        data = StringUtil.item_to_json(Status.get_current_status_by_platform(platform))
        return data

class get_current_status:
    def GET(self):
        data = StringUtil.item_to_json(Status.get_current_status())
        return data

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()