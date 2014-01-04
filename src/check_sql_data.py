#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import sqlite3
con = sqlite3.connect('app.db')
cur = con.cursor()
cur.execute('select count(*) from app_info')
apps = cur.fetchall()
for app in apps:
	print app