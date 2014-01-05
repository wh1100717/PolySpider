#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from PolySpider.config import Config
from PolySpider.util import SqliteUtil

def get_app_by_app_name(app_name):
    cur = Config.DB_CON.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def insert_app(item):
    #插入数据
    print '数据库ps_app插入数据'
    sql = '''INSERT INTO ps_app values(null,?,?,?)'''
    data = [(
         item['app_name'],
         item['author'],
         item['category'])]
    SqliteUtil.save(Config.DB_CON, sql, data)
    cur = Config.DB_CON.cursor()
    cur.execute("select last_insert_rowid() from ps_app")
    return cur.fetchall[0][0]

def update_app_author(id, author):
    #更新数据
    print "数据库更新数据"
    sql = '''UPDATE ps_app set author = ? where id = ?'''
    data = [(author, id)]
    SqliteUtil.update(Config.DB_CON, sql, data)

def update_app_category(id, category):
    #更新数据
    print "数据库更新数据"
    sql = '''UPDATE ps_app set category = ? where id = ?'''
    data = [(category, id)]
    SqliteUtil.update(Config.DB_CON, sql, data)
