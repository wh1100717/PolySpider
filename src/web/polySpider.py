#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import web
import os
import sys
if sys.path[-1].split("\\")[-1] != "src": 
    c_path = os.getcwd()
    sys.path.append(c_path[:c_path.rfind("\\")])

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
    '/app/get_app_by_app_name/?','get_app_by_app_name',
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
        return render.data()

class get_app_list:
    def GET(self):
        data = '''
                [
                    ["Firefox",   45.0],
                    ["IE",       26.8],
                    {
                        "name": "Chrome",
                        "y": 12.8,
                        "sliced": true,
                        "selected": true
                    },
                    ["Safari",    8.5],
                    ["Opera",     6.2],
                    ["Others",   0.7]
                ]
                '''
        return data

class get_app_by_app_name:
    def GET(self):
        result = App.get_app_by_app_name()
        print result
        return "Success"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()