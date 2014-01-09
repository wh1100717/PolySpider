import datetime
#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3
import datetime

from PolySpider.config import Config
from PolySpider.util import SqliteUtil

def get_today_status(platform):
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
    sql = '''
            UPDATE ps_status set 
                crawled_app_count = ?,
                new_app_count = ?,
                update_app_count = ?
            where id = ?'''
    SqliteUtil.update(sql, data)
    
def get_status_list():
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_status"
    cur.execute(sql)
    status = cur.fetchall()
    return status

def get_status_list_by_platform(platform):
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_status where platform = ?"
    cur.execute(sql,(platform,))
    status = cur.fetchall()
    return status

def get_current_status_by_platform(platform):
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

def create_fade_status(startdate):
    sql = '''INSERT INTO ps_status values(null,?,?,0,0,0)'''
    data = (platform, today)
    id = SqliteUtil.save_return_id(sql, data)
    status = [(id,platform,today,0,0,0)]

