#!/usr/bin/env python
#coding:gbk

import sqlite3
con = sqlite3.connect('app.db')
cur = con.cursor()
cur.execute('select apk_url from app_info')
apps = cur.fetchall()
for app in apps:
	print app