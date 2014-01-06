#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import web

DB = web.database(dbn='sqlite', db='app.db')
cache = False