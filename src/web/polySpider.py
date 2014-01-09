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
    '/status/get_status_list_by_platform/(.+)','get_status_list_by_platform',
    '/status/get_current_status_by_platform/(.+)','get_current_status_by_platform',
    
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
        data  = App.count_app_categroy_sum()
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

class get_status_list_by_platform:
    def GET(self, platform):
        data = StringUtil.item_to_json(Status.get_status_list_by_platform(platform))
        data = '[[3,"xiaomi","2014-01-07",85,0,0],[5,"xiaomi","2014-01-08",100,15,17],[10,"xiaomi","2014-01-09",115,235,64],[10,"xiaomi","2014-01-10",125,343,132],[10,"xiaomi","2014-01-11",135,253,523],[10,"xiaomi","2014-01-12",145,546,654],[10,"xiaomi","2014-01-13",135,324,313],[10,"xiaomi","2014-01-14",165,231,653],[10,"xiaomi","2014-01-15",185,165,756],[10,"xiaomi","2014-01-16",125,111,432],[10,"xiaomi","2014-01-17",115,753,422],[10,"xiaomi","2014-01-18",145,234,814],[10,"xiaomi","2014-01-19",215,523,257],[10,"xiaomi","2014-01-20",245,423,857],[10,"xiaomi","2014-01-21",535,234,147],[10,"xiaomi","2014-01-22",645,132,457],[10,"xiaomi","2014-01-23",345,564,167]]'
        return data

class get_current_status_by_platform:
    def GET(self,platform):
        data = StringUtil.item_to_json(Status.get_current_status_by_platform(platform))
        return data

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()