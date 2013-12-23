import os
import xml.dom.minidom
def readxml(name):
    xmlname=name.spilt('\.')[0]+'\.xml'
    os.system("..\\apk unzip "+name+"  AndroidManifest.xml ")
    os.system("..\\apk ren AndroidManifest.xml "+xmlname)
    print "get apkxml ok"
    doc = minidom.parse(xmlname)
    node = doc.getElementsByTagName("manifest")
    packagename = node[0].getAttribute("package")
    return packagename