#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
import sqlite3

def get_app_detail_by_item(item):
    '''
    ##根据app_id | version | platform来唯一确认app_detail标识
    *   input: item
    *   output: app_detail
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_app_detail where app_id = ? and version = ? and platform = ?"
    cur.execute(sql,(item['app_id'], item['version'], item['platform']))
    return cur.fetchall()
def insert_app_detail(item):
    '''
    ##插入数据
    *   input: item
    '''
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
    '''
    data = [
            'version':item['version'],
         'platform':item['platform'],
         'apk_url':item['apk_url'],
         'apk_size':item['apk_size'],
         'package_name':item['pakage_name'],
         'cover':item['cover'],
         'rating_point':item['rating_point'],
         'rating_count':item['rating_count'],
         'android_version':item['android_version'],
         'download_times':item['download_times'],
         'description':item['description'],
         'img_url':item['imgs_url'],
         'last_update':item['last_update']]
    '''
def get_app_detail_by_id(app_id):
    '''
    ##根据app_id来查询对应的detail
    *   input: app_id
    *   output: app_detail
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select * from ps_app_detail where app_id = ?'''
    cur.execute(sql,app_id)
    return cur.fetchall()
def get_platform_app_count():
    '''
    ##查询不同平台app数量 不同版本算多个
    *   output: [platform, count(app_id)]
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select platform,count(app_id) from ps_app_detail group by platform'''
    cur.execute(sql)
    return cur.fetchall()
def get_platform_app_count_unique():
    '''
    ##查询不同平台app数量 不同版本算一个
    *   output: [platform, count(app_id)]
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select platform,count(*) from (select platform,app_id from ps_app_detail group by app_id) group by platform'''
    cur.execute(sql)
    return cur.fetchall()
def get_app_detail_list(page_index = 1,row_number = 100,sort = "id",order = "asc"):
    '''
    ##查询不同平台app数量 不同版本算一个
    *   page_index代表页数 | row_number显示行数 | sort按某条件排序 | order升序降序
    *   output: app_dtail type of List
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select * from ps_app join ps_app_detail where ps_app.id=ps_app_detail.app_id order by ? limit ? offset ? '''
    startnum=(int(page_index)-1)*int(row_number)
    temp = sort+' '+order
    
    cur.execute(sql,(temp,row_number,startnum))
    return cur.fetchall()