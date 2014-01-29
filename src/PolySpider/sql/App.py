#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
from PolySpider.util import RedisUtil
redis_client = RedisUtil.RedisClient()
def get_app_by_app_name(app_name):
    '''
    ##根据app_name来获取app record
    *   input: app_name
    *   output: app
    '''
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def get_app_by_id(id):
    '''
    ##根据app_id来获取app record
    *   input: id
    *   output: app
    '''
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select * from ps_app where id = ?"
    cur.execute(sql,(id,))
    return cur.fetchall()

def insert_app(item):
    '''
    ##插入app数据
    *   input: item
    *   output: id
    '''
    sql = '''INSERT INTO ps_app values(null,?,?,?)'''
    data = (item['app_name'], item['author'], item['category'])
#    id = SqliteUtil.save_return_id(sql, data)
    id = 1
    print "_____________"
    
    print redis_client.hset('app::' + str(id),'app_name',item['app_name'])
    print "_________________"
    return id

def update_app_author(id, author):
    '''
    ##更新app中的作者信息
    *   input: id | author
    '''
    sql = '''UPDATE ps_app set author = ? where id = ?'''
    data = [(author, id)]
    SqliteUtil.update(sql, data)
    #redis.hset(id,'author',author)

def update_app_category(id, category):
    '''
    ##更新app中的分类信息
    *   input: id | category
    '''
    sql = '''UPDATE ps_app set category = ? where id = ?'''
    data = [(category, id)]
    SqliteUtil.update(sql, data)
     #redis.hset(id,'category',category)
    
def search_app_category(id):
    '''
    ##根据id查找该应用的分类
    *   input: id
    *   output: category
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql = "select category from ps_app where id= ?"
    cur.execute(sql,(id,))
    return cur.fetchall()
    
def get_app_categories():
    '''
    ##获取所有应用的分类信息
    *   output: categories type of List
    '''
    #某个分类下app的总数
    sql = '''select category from ps_app '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    cur.execute(sql)
    return cur.fetchall()
            
def get_app_list(page_index = 1,row_number = 100,sort = "id",order = "asc"):
    '''
    ##获取所有应用列表
    *   page_index代表页数 | row_number显示行数 | sort按某条件排序 | order升序降序
    *   input: page_index | row_number | sort | order
    *   output: apps type of List
    '''
    con = sqlite3.connect(Config.get_sqlite_path())
    cur = con.cursor()
    sql='''select * from ps_app order by ? limit ? offset ?'''
    startnum=(int(page_index)-1)*int(row_number)
    temp = sort+' '+order
    cur.execute(sql,(temp,row_number,startnum,))
    return cur.fetchall()
