#!/usr/bin/env python
#coding:gbk

import os
import yaml
import shutil
import platform

def apkTool(apk_name):  
    apk_file_path='apk/' + apk_name
    os.system('java -jar PolySpider\\tools\\apktool.jar d ' + apk_file_path + " apk\\unzip\\" + apk_name)
    return True

def unzipApk(apk_name):
    #增加系统判断，如果为Windows系统，则调用PolySpider/tools/unzip.exe进行解压缩
    if platform.system() == 'Windows':
        os.system('PolySpider\\tools\\unzip.exe apk\\' + apk_name +  '"AndroidManifest.xml" -d apk\\unzip\\' + apk_name)
    else:
        os.system('unzip apk\\' + apk_name +  '"AndroidManifest.xml" -d apk\\unzip\\' + apk_name)
    return 'apk\\unzip\\' + apk_name

def normalizeManifest(apk_name):
    unzipApk(apk_name)
    os.system('java -jar PolySpider\\tools\\AXMLPrinter2.jar apk\\unzip\\' + apk_name + "\\AndroidManifest.xml>apk\\unzip\\" + apk_name + "\\info_list.xml")
    return "apk\\unzip\\" + apk_name + "\\info_list.xml"

def getInfoList(apk_name):
    if apkTool(apk_name):
        with open('apk/unzip/' + apk_name + "/apktool.yml") as f:
            info_list = yaml.load(f)
        shutil.rmtree('apk/unzip/' + apk_name)
    return info_list

def getApkPakageName(apk_name):
    info_list = getInfoList(apk_name)
    return info_list['packageInfo']['orig_package']
