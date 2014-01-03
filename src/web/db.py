#!/usr/bin/env python
#coding:gbk

import config

def listing(**k):
    return config.DB.select('items', **k)
