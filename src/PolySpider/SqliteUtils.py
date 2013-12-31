#!/usr/bin/env python
#coding:gbk

import sqlite3
import os
from PolySpider import Config

def check_sql(sql):
    if not sql or sql == '': 
        print('the [{}] is empty or equal None!'.format(sql))
        return False
    else: return True

def get_conn(path):
    '''
    创建数据库连接
    如果path存在并且是一个文件路径，则创建文件数据库链接
    否则创建内存数据库链接
    '''
    return sqlite3.connect(path)
    
def get_cursor(conn):
    '''
    获取游标，如果conn为空，则获取内存游标
    '''
    return conn.cursor() if conn else get_conn('').cursor()
    
def close_all(conn, cu):
    '''
    关闭数据库游标对象和数据库连接对象
    '''
    try:
        if not cu: cu.close()
    finally:
        if conn: conn.close()

def is_table_exist(cur, table_name):
    return True if cur.execute("SELECT count(*) FROM sqlite_master WHERE type= 'table' and name = ? ",(table_name,)).fetchone()[0] > 0 else False

def create_table(conn, sql):
    '''
    创建数据库表
    '''
    if not check_sql(sql): return
    cu = get_cursor(conn)
    if Config.SHOW_SQL: print('创建表\n执行sql:[{}]'.format(sql))
    cu.execute(sql)
    conn.commit()
    print('创建数据库表成功!')
            
def drop_table(conn, table):
    '''如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！'''
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS ' + table
        if Config.SHOW_SQL: print('执行sql:[{}]'.format(sql))
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('删除数据库表[{}]成功!'.format(table))
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def save_or_update(conn, sql, data):
    '''
    插入数据
    data为要插入的数据，格式为list，可以存放多条数据
    '''
    if not check_sql(sql): return
    if not data: return
    cu = get_cursor(conn)
    for d in data:
        if Config.SHOW_SQL: print('插入或更新数据\n执行sql:[{}],参数:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
        
def delete(conn, sql, data):
    '''删除数据'''
    if not check_sql(sql): return
    if not data: return
    cu = get_cursor(conn)
    for d in data:
        if Config.SHOW_SQL: print('删除数据\n执行sql:[{}],参数:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
        
def getItemByAppName(cur, app_name):
    sql = "select * from app_info where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()
    
def fetchall(conn, sql, conditions):
    '''
    查询所有数据
    conditions是where的限制条件
    '''
    if not check_sql(sql): return
    cu,cons = get_cursor(conn),(conditions,)
    cu.execute(sql, cons) if data else cu.execute(sql)
    if Config.SHOW_SQL: print('查询所有数据\n执行sql:[{}]'.format(sql,conditions))
    return cu.fetchall()

def checkAppInfoExist(conn):
    #如果表不存在，则创建表
    cur = get_cursor(conn)
    if  not is_table_exist(cur, 'app_info'):
        sql_table_create = '''
            CREATE TABLE app_info(
            id INTEGER PRIMARY KEY,
            apk_url TEXT,
            pakage_name VARCHAR(32),
            app_name VARCHAR(32),
            cover VARCHAR(32),
            version VARCHAR(32),
            rating_star VARCHAR(32),
            rating_count VARCHAR(32),
            category VARCHAR(32),
            android_version VARCHAR(32),
            download_times VARCHAR(32),
            author VARCHAR(32),
            last_update TEXT,
            description TEXT,
            imgs_url TEXT,
            apk_size VARCHAR(32)
            )
        '''
        create_table(conn,sql_table_create)
