#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3

from PolySpider.config import Config
from PolySpider.util import SqliteUtil
from PolySpider.util import CategoryUtil
def get_app_by_app_name(app_name):
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def get_app_by_id(id):
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where id = ?"
    cur.execute(sql,(id,))
    return cur.fetchall()

def insert_app(item):
    #插入数据
    print '数据库ps_app插入数据'
    sql = '''INSERT INTO ps_app values(null,?,?,?)'''
    data = (item['app_name'], item['author'], item['category'])
    result = SqliteUtil.save_return_id(sql, data)
    return result

def update_app_author(id, author):
    #更新数据
    print "数据库更新数据"
    sql = '''UPDATE ps_app set author = ? where id = ?'''
    data = [(author, id)]
    SqliteUtil.update(sql, data)

def update_app_category(id, category):
    #更新数据
    print "数据库更新数据"
    sql = '''UPDATE ps_app set category = ? where id = ?'''
    data = [(category, id)]
    SqliteUtil.update(sql, data)
def search_app_category(id):
    #查找某个app的分类
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select category from ps_app where id= ?"
    cur.execute(sql,(id,))
    
    
    return cur.fetchall()
def count_app_categroy_sum():
    #某个分类下app的总数
    sql = '''select category from ps_app '''
    count_categorys={}
    count_categorys['1000']=0
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    cur.execute(sql)
    categorys =cur.fetchall()
    for category in categorys:
        
        for temp in category[0].split(','):
            app_category = temp.split(':')[0]
            if temp:
                if app_category!='':
                    if not count_categorys.get(app_category):
                        count_categorys[app_category]=1
                    else:
                        count_categorys[app_category]=int(count_categorys[app_category])+1
                else:
                    count_categorys['1000']=count_categorys['1000']+1
    data="["
    for count_category in count_categorys:
        data=data+'["'+unicode(str(CategoryUtil.get_category_name_by_id(count_category)))+'",'+str(count_categorys[count_category])+"],"
    data=data[:-1]+"]"
    return data
            
            
def get_app_list(page_index = 1,row_number = 13000,sort = "id",order = "asc"):
    #应用列表
    #page_index代表页数 row_number显示行数sort按某条件排序order升序降序
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql='''select * from ps_app order by ? limit ? offset ?'''
    startnum=(int(page_index)-1)*int(row_number)
    temp = sort+' '+order
    cur.execute(sql,(temp,row_number,startnum,))
    datas = cur.fetchall()
    for index in range(len(datas)):
        data = list(datas[index])
        data[3]=CategoryUtil.get_category_name_by_id(data[3][0:4])
        datas[index]=tuple(data)
    return datas
