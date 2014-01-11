#!/usr/bin/env python
# -*- coding: utf-8 -*-  

def item_to_json(item):
    '''
    对数据库中取到的数据进行json格式化处理
    '''
    print item
    if isinstance(item, int):
        return str(item)
    elif isinstance(item, str):
        return '"' + item + '"'
    elif isinstance(item, tuple):
        return item_to_json(list(item))
    elif isinstance(item, list):
        result = "["
        for i in item:
            result += item_to_json(i) + ","
        return result[:-1] + "]"
    else:
        return '"'+ str(item) + '"'
