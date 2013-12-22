#!/usr/bin/env python
#coding:gbk

def cmpVersion(oldVersion, newVersion):
    '''
    比较版本号
    如果oldVersion大于newVersion，则返回True,反之则返回False
    1.1.0和1.2.0比较，返回False
    1.1.1.1和1.1.1比较，返回True
    1.1和1.1.1比较，返回False
    '''
    old_vs = oldVersion.strip().split(".")
    new_vs = newVersion.strip().split(".")
    for i in range(len(old_vs)):
        if i >= len(new_vs): return True
	old_v = int(old_vs[i])
	new_v = int(new_vs[i])
	if new_v > old_v:
		return False
	elif old_v > new_v:
		return True
    if len(old_vs) < len(new_vs):
        return False
    else:
        return True