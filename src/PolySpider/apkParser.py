import os
import yaml
import shutil

def apkTool(apk_name):  
    apk_file_path='apk/' + apk_name
    os.system('PolySpider\\tools\\apktool.jar d ' + apk_file_path + " apk\\unzip\\" + apk_name)
    return True

def getInfoList(apk_name):
    if apkTool(apk_name):
        with open('apk/unzip/' + apk_name + "/apktool.yml") as f:
            info_list = yaml.load(f)
        shutil.rmtree('apk/unzip/' + apk_name)
    return info_list

def getApkPakageName(apk_name):
    info_list = getInfoList(apk_name)
    return info_list['packageInfo']['orig_package']
