#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import sqlite3
    
from PolySpider.config import Config

def check_sql(sql):
    '''
    检查sql语句是否为空
    '''
    if not sql or sql == '': 
        print('the [{}] is empty or equal None!'.format(sql))
        return False
    else: return True
    
def is_table_exist(table_name):
    '''
    检查table_name的数据库表是否存在
    '''
    con = sqlite3.connect(Config.SQLITE_PATH)
    return True if con.cursor().execute("SELECT count(*) FROM sqlite_master WHERE type= 'table' and name = ? ",(table_name,)).fetchone()[0] > 0 else False

def checkTableExist():
    '''
    检查数据库中是否存在表
    如果数据库中无ps_app和ps_app_detail表，则创建表
    '''
    if not is_table_exist('ps_app'):
        sql_table_create = '''
            CREATE TABLE ps_app(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name VARCHAR(32),
                author VARCHAR(32),
                category VARCHAR(32)
            );
        '''
        create_table(sql_table_create)
    if not is_table_exist('ps_app_detail'):
        sql_table_create = '''
            CREATE TABLE ps_app_detail(
                app_id INTEGER,
                version VARCHAR(32),
                platform VARCHAR(32),
                apk_url TEXT,
                apk_size VARCHAR(32),
                pakage_name VARCHAR(32),
                cover VARCHAR(32),
                rating_point VARCHAR(32),
                rating_count VARCHAR(32),
                android_version VARCHAR(32),
                download_times VARCHAR(32),
                description TEXT,
                imgs_url TEXT,
                last_update TEXT,
                primary key (app_id, version, platform)
            );
        '''
        create_table(sql_table_create)
    if not is_table_exist('ps_status'):
        sql_table_create = '''
            CREATE TABLE ps_status(
                id INTEGER PRIMARY KEY,
                platform VARCHAR(32),
                create_date TEXT,
                crawled_app_count INTEGER,
                new_app_count INTEGER,
                update_app_count INTEGER
            );
        '''
        create_table(sql_table_create)

def close_all(con):
    '''
    关闭数据库游标对象和数据库连接对象
    '''
    try:
        if not con.cursor(): con.cursor().close()
    finally:
        if con: con.close()

def execute_sql(sql, data = ""):
    '''
    执行sql语句
    data默认为空,data为list，可执行多条数据操作
    '''
    con = sqlite3.connect(Config.SQLITE_PATH)
    if not check_sql(sql): return
    cur = con.cursor()
    if data == "":
        cur.execute(sql)
    else:
        for d in data:
            if Config.SHOW_SQL: print('执行sql:[{}],参数:[{}]'.format(sql, d))
            cur.execute(sql, d)
    con.commit()
    close_all(con)

def create_table(sql):
    '''
    创建数据库表
    '''
    execute_sql(sql)
    print('创建数据库表成功!')

def drop_table(table):
    '''
    如果表存在,则删除表，如果表中存在数据的时候，使用该方法的时候要慎用！
    '''
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS ' + table
        execute_sql(sql)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def save(sql, data):
    '''
    插入数据
    data为要插入的数据，格式为list，可以存放多条数据
    '''
    if not data: return
    execute_sql(sql, data)
    print('插入数据成功!')

def save_return_id(sql, data):
    '''
    插入数据
    data为要插入的数据
    返回插入生成的id，要求id为INTEGER PRIMARY KEY AUTOINCREMENT格式
    '''
    id = 0
    if not data: return
    con = sqlite3.connect(Config.SQLITE_PATH)
    if not check_sql(sql): return
    cur = con.cursor()
    if Config.SHOW_SQL: print('执行sql:[{}],参数:[{}]'.format(sql, data))
    cur.execute(sql, data)
    id = cur.lastrowid
    con.commit()
    close_all(con)
    return id
    
def update(sql, data):
    '''
    更新数据
    data为要插入的数据，格式为list，可以存放多条数据    
    '''
    if not data: return
    execute_sql(sql, data)
    print('更新数据成功!')
        
def delete(sql, data):
    '''
    删除数据
    '''
    if not data: return
    execute_sql(sql, data)
    print('删除数据成功!')

###################################################################



def getItemByAppName(con, app_name):
    cur = get_cursor(con)
    sql = "select * from app_info where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()
    
def fetchall(con, sql, conditions):
    '''
    查询所有数据
    conditions是where的限制条件
    '''
    if not check_sql(sql): return
    cu,cons = get_cursor(con),(conditions,)
    cu.execute(sql, cons) if data else cu.execute(sql)
    if Config.SHOW_SQL: print('查询所有数据\n执行sql:[{}]'.format(sql,conditions))
    return cu.fetchall()

