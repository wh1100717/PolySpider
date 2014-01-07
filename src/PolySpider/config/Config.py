#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os
import sys
if sys.path[-1].split("\\")[-1] != "src": 
    c_path = os.getcwd()
    if "\\" in c_path:
        sys.path.append(c_path[:c_path.rfind("\\")])
    else:
        sys.path.append(c_path[:c_path.rfind("/")])
    
#Sqlite3 Configuration
if "win" in sys.platform:
    SQLITE_PATH = sys.path[-1] + "\\" + "app.db"
else:
    SQLITE_PATH = sys.path[-1] + "/" + "app.db"
SHOW_SQL = False #True则会在控制台显示详细的SQL查询

#App Star Constant
APPSTAR_MAX_APPS = 30000

#BaiduYun AK && SK
'''这里需要填写BaiYun的公钥AK，私钥SK和Bucket'''
BAIDU_AK = ''
BAIDU_SK = ''
BAIDU_BUCKET = ''

#UpYun
'''这里需要填写申请下来的又拍云所对应的bucket的用户名和密码'''
UPYUN_USERNAME = ''
UPYUN_PASSWORD = ''
UPYUN_BUCKET = ''