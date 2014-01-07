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

from view import render

render = web.template.render('templates/', base='layout')
render_without_layout = web.template.render('templates/')

urls = (
    '/(home/?)?', 'home',
    '/state/?', 'state',
    '/chart/?', 'chart',
    '/data/?', 'data',
    '/app/get_app_list/data.json', 'get_app_list',
    '/app/count_app_categroy_sum/?','count_app_categroy_sum',
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
        print apps
        return render.data(apps)

class get_app_list:
    def GET(self):
        data  = App.count_app_categroy_sum()
        return data

class count_app_categroy_sum:
    def GET(self):
        result = App.count_app_categroy_sum()
        
        return "Success"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()