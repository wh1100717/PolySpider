#!/usr/bin/env python
#coding:gbk
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
		return False
	elif old_v > new_v:
		return True
    if len(old_vs) < len(new_vs):
        return False
    else:
        return True
'''
下载进度条，和文件下载
'''
def progressbar(url,fileName):
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
    
     