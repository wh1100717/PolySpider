#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3
import datetime
from PolySpider.config import Config
from PolySpider.util import SqliteUtil

def get_today_status(platform):
    '''
    ##根据平台获取当前该平台的爬虫状态，如果今天没有Status数据，则创建一条Status记录
    *   input: platform
    *   output: status
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    today = datetime.date.today()
    sql = "select * from ps_status where platform = ? and create_date = ?"
    cur.execute(sql,(platform,today))
    status = cur.fetchall()
    if status == []:
        sql = '''INSERT INTO ps_status values(null,?,?,0,0,0)'''
        data = (platform, today)
        id = SqliteUtil.save_return_id(sql, data)
        status = [(id,platform,today,0,0,0)]
    return status[0]
def update_status(data):
    '''
    ##更新status
    *   input: data(包含crawled_app_count | new_app_count | update_app_count)
    '''
    sql = '''
        UPDATE ps_status set 
            crawled_app_count = ?,
            new_app_count = ?,
            update_app_count = ?
        where id = ?
        '''
    SqliteUtil.update(sql, data)
def get_status_list():
    '''
    ##获取全部status列表
    *   output: status type of List
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_status"
    cur.execute(sql)
    status = cur.fetchall()
    return status
def get_status_list_by_platform(platform):
    '''
    ##获取某一平台的status列表
    *   input:  platform
    *   output: status type of List
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_status where platform = ?"
    cur.execute(sql,(platform,))
    status = cur.fetchall()
    return status
def get_current_status_by_platform(platform):
    '''
    ##获取今天某一平台的status
    *   input:  platform
    *   output: status
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    today = datetime.date.today()
    sql = "select * from ps_status where platform = ? and create_date = ?"
    cur.execute(sql,(platform,today))
    status = cur.fetchall()
    if status == []:
        sql = '''INSERT INTO ps_status values(null,?,?,0,0,0)'''
        data = (platform, today)
        id = SqliteUtil.save_return_id(sql, data)
        status = [(id,platform,today,0,0,0)]
    return status[0]
def get_current_status():
    '''
    ##获取今天所有平台的status列表
    *   output: status type of List
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    today = datetime.date.today()
    sql = "select * from ps_status where create_date = ?"
    cur.execute(sql,(today,))
    status = cur.fetchall()
    return status