import datetime
#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3
import datetime

from PolySpider.config import Config
from PolySpider.util import SqliteUtil

def get_app_by_app_name(app_name):
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def get_today_status(platform):
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    today = datetime.date.today()
    sql = "select * from ps_status where platform = ? and create_time = ?"
    cur.execute(sql,(platform,today))
    status = cur.fetchall()[0]
    if status == "":
        sql = '''INSERT INTO ps_status values(null,?,?,0,0,0)'''
        data = (platform, today)
        id = SqliteUtil.save_return_id(sql, data)
        status = (id,platform,today,0,0,0)
    return status

def update_status(data):
    sql = '''
            UPDATE ps_status set 
                crawled_app_count = ?,
                new_app_count = ?,
                update_app_count = ?
            where id = ?'''
    SqliteUtil.update(sql, data)