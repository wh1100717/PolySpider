#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib
from progressbar import *
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
            print "当前版本：%s | 抓取的应用版本：%s : 执行更新操作" %(oldVersion, newVersion)
            return False
	elif old_v > new_v:
            print "当前版本：%s | 抓取的应用版本：%s : 不执行更新操作" %(oldVersion, newVersion)
            return True
    if len(old_vs) < len(new_vs):
        print "当前版本：%s | 抓取的应用版本：%s : 执行更新操作" %(oldVersion, newVersion)
        return False
    else:
        print "当前版本：%s | 抓取的应用版本：%s : 不执行更新操作" %(oldVersion, newVersion)
        return True

def normalizeVersion(versionInput):
    '''
    对抓取到的版本号进行格式化处理
    保证版本号的格式为XXX.XXX.XXX
    其中X为数字
    注1：把所有非数字过滤掉
    注2：对于带有字母的版本号同样舍弃，目前不知道是否有这方面版本号记录的需求
    '''
    if not versionInput: return ""
    result = ""
    for digit in versionInput:
        if digit in "1234567890.":
            result += digit

    return result

def progressbar(url,fileName):
    '''
    下载进度条，和文件下载
    '''
    file=urllib.urlopen(url)
    totalSize=file.info().getheader("content-length")
    count=1000
    blockSize=int(totalSize)/int(count)
    widgets = [' <<<', Bar(), '>>> ',Percentage(),' ', ETA() ,' ' ,  FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets)

    def dlProgress(count, blockSize, totalSize):
        if pbar.maxval is None:
            pbar.maxval = totalSize
            pbar.start()
        pbar.update(min(count*blockSize, totalSize))
    urllib.urlretrieve(url, fileName, reporthook=dlProgress)
    pbar.finish()

def dropBrackets(str):
    str=str.encode('utf8')
    str = normalizeString(str)
    while '(' in str:
        startPoint = str.find('(')
        endPoint = str.rfind(')')
        str = str[:startPoint] if endPoint == -1 else str[:startPoint] + str[endPoint+1:]
    return str.strip().decode('utf8')
def normalizeString(str):
    str=str.encode('utf8')
    normalizedStr = {
        '\t':'',
        '\n':'',
        '\r':'',
        '｛':'{',
        '｝':'}',
        '（':'(',
        '）':')',
        '【':'[',
        '】':']',
        '？':'?',
        '‘':'\'',
        '’':'\'',
        '“':'"',
        '”':'"',
        '：':':'
    }
    for key in normalizedStr.keys():
        str = str.replace(key,normalizedStr[key])
    return str.decode('utf8')
def download_time_normalize(download_time):
    download_time=download_time.encode('utf8')
    download_time=download_time.replace('+','')
    download_time=download_time.replace('小于','')
    if download_time.find('.')<0:
        download_time=download_time.replace('万','0000')
        download_time=download_time.replace('千','000')
        download_time=download_time.replace('千万','00000000')
        download_time=download_time.replace('亿','000000000')
    if download_time.find('千万')>0:
        download_time=str(int(float(download_time[0:download_time.find('千')])*10000000))
    if download_time.find('千')>0:
        download_time=str(int(float(download_time[0:download_time.find('千')])*1000))
    if download_time.find('万')>0:
        download_time=str(int(float(download_time[0:download_time.find('万')])*10000))
    if download_time.find('亿')>0:
        download_time=str(int(float(download_time[0:download_time.find('亿')])*100000000))
    return download_time.decode('utf8')
    