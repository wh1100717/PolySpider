#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import web
from view import render

render = web.template.render('templates/')

urls = (
    '/(home/?)?', 'home',
    '/state/?', 'state',
    '/chart/?', 'chart',
    '/data/?', 'data'
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

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()