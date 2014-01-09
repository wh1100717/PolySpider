#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
from PolySpider.util import CategoryUtil
import sqlite3

def get_app_detail_by_item(item):
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    print item['app_id']
    sql = "select * from ps_app_detail where app_id = ? and version = ? and platform = ?"
    cur.execute(sql,(item['app_id'], item['version'], item['platform']))
    return cur.fetchall()

def insert_app_detail(item):
    #插入数据
    print '数据库ps_app_detail插入数据'
    sql = '''INSERT INTO ps_app_detail values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    data = [(
         item['app_id'],
         item['version'],
         item['platform'],
         item['apk_url'],
         item['apk_size'],
         item['pakage_name'],
         item['cover'],
         item['rating_point'],
         item['rating_count'],
         item['android_version'],
         item['download_times'],
         item['description'],
         item['imgs_url'],
         item['last_update'],)]
    SqliteUtil.save(sql, data)
    




def get_app_detail_by_id(id):
    #根据id查询app_detail
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select * from ps_app_detail where app_id = ?'''
    cur.execute(sql,id)
    return cur.fetchall()

def get_platform_app_count():
    #查询不同平台app数量 不同版本算多个
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select platform,count(app_id) from ps_app_detail group by platform'''
    platform_appnum="["
    cur.execute(sql)
    return cur.fetchall()

def get_platform_app_count_unique():
    #查询不同平台app数量 不同版本算一个
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select platform,count(*) from (select platform,app_id from ps_app_detail group by app_id) group by platform'''
    platform_appnum="["
    cur.execute(sql)
    return cur.fetchall()

def get_app_detail_list():
    #应用列表
    #page_index代表页数 row_number显示行数sort按某条件排序order升序降序
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select * from ps_app join ps_app_detail where ps_app.id=ps_app_detail.app_id limit 100'''
    cur.execute(sql)
    return cur.fetchall()

