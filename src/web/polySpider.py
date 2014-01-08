#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import web
import os
import sys
if sys.path[-1].split("\\")[-1] != "src": 
    c_path = os.getcwd()
    if "win" in sys.platform:
        sys.path.append(c_path[:c_path.rfind("\\")])
    else:
        sys.path.append(c_path[:c_path.rfind("/")])
from PolySpider.sql import App
from PolySpider.sql import AppDetail

from view import render

render = web.template.render('templates/', base='layout')
render_without_layout = web.template.render('templates/')

urls = (
    '/(home/?)?', 'home',
    '/state/?', 'state',
    '/chart/?', 'chart',
    '/data/?', 'data',
    '/app/get_category_chart/?', 'get_category_chart',
    '/app/get_platform_chart/?','get_platform_chart',
    '/app/get_platform_chart_unique/?','get_platform_chart_unique',
    
)

class home:
    def GET(self,name):
        return render.home()

class state:
    def GET(self):
        return render.state()

class chart:
    def GET(self):
        return render.chart()

class data:
    def GET(self):
        apps = App.get_app_list()
        app_details=AppDetail.get_app_detail_list()
        data=[apps,app_details]
        return render.data(data)

class get_category_chart:
    def GET(self):
        data  = App.count_app_categroy_sum()
        return data

class get_platform_chart:
    def GET(self):
        data = AppDetail.get_platform_app_count()
        return data
class get_platform_chart_unique:
    def GET(self):
        data = AppDetail.get_platform_app_count_unique()
        return data


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()