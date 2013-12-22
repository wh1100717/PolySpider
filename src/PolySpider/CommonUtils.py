#!/usr/bin/env python
#coding:gbk

def cmpVersion(oldVersion, newVersion):
    old_vs = oldVersion.strip().split(".")
    new_vs = newVersion.strip().split(".")
    for i in range(len(old_vs)):
	old_v = int(old_vs[i])
	new_v = int(new_vs[i])
	if new_v > old_v:
		return False
	elif old_v > new_v:
		return True
    return True