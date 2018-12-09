import os
import json
import re
import time
import sys
import requests
from qqrobot.settings import BASE_DIR

PYTHON_SCRIPT = 'python_script'
SCRIPT_DIR = 'script'
IMAGES = 'image'
FONTS = 'fonts'
IMAGES_DIR = os.path.join(os.path.join(BASE_DIR,SCRIPT_DIR),IMAGES)
PYTHON_SCRIPT_DIR = os.path.join(os.path.join(BASE_DIR,SCRIPT_DIR),PYTHON_SCRIPT)
FONTS_DIR = os.path.join(os.path.join(BASE_DIR,SCRIPT_DIR),FONTS)
BUFFSIZE = 4096

def checkPythonFileExists(fileName):
    return fileExists(os.path.join(PYTHON_SCRIPT_DIR,fileName))

def pythonScriptReName(source,newName):
    return reName(os.path.join(PYTHON_SCRIPT_DIR,source),newName)

def reName(source,newName):
    if fileExists(source):
        path, sourceName = os.path.split(source)
        newNamePath = os.path.join(path, newName)
        os.rename(source,newNamePath)
        return True
    else:
        return False

def translate(text):
    text = text.replace('&#91;', '[')
    text = text.replace('&#93;', ']')
    text = text.replace('&amp;', '&')
    return text

def dirExists(path):
    if os.path.exists(path) and os.path.isdir(path) :
        return True
    else:
        return False

def dirCreate(path):
    if not dirExists(path):
        os.mkdir(path)
        return True
    else:
        return False

def fileExists(path):
    if os.path.exists(path) and os.path.isfile(path):
        return True
    else:
        return False

def importScript(file):
    # import numpy
    # import matplotlib
    # import matplotlib.pyplot
    # sys.modules['os'] = None
    return __import__(file)

def fileCreate(path):
    if fileExists(path):
        return False
    else:
        os.mknod(path)
        return True

def filterFileExtension(files,extendName):
    L = []
    for file in files:
        _,path = os.path.split(file)
        fileName,extendname = os.path.splitext(path)
        if extendname == extendName:
            L.append(fileName)
    return L


def getPythonScriptFiles():
    return getFiles(PYTHON_SCRIPT)

def clearScript(module_name):
    # imp.reload('os')
    del sys.modules[module_name]

def extractPic(text):
    results = re.findall(r'\[CQ:image,file=(.*?),url=(.*?)\]',text)
    dic = {}
    for result in results:
        dic[result[0]] = result[1]
    return dic

def fromUrlDownPic(name,url):
    path = os.path.join(IMAGES_DIR,name)
    res = requests.get(url)
    saveFile(path,res.content)

def replacePic(text):
    replace = '[CQ:image,file=file:///%s\g<file>,url=\g<url>]'%IMAGES_DIR
    return re.sub(r'\[CQ:image,file=(?P<file>.*?),url=(?P<url>.*?)\]',replace, text)

def savePic(text):
    pics = extractPic(text)
    for name in pics:
        fromUrlDownPic(name,pics[name])

def getImagesFiles():
    return getFiles(IMAGES)

def getFiles(path):
    return os.listdir(path)

def savePythonScriptFile(fileName,text):
    saveFile(os.path.join(PYTHON_SCRIPT_DIR,fileName),text,'w')

def saveFile(path,data,method='wb'):
    with open(path,method)as f:
        f.write(data)

def readPythonScriptFile(fileName):
    obj = readFile(os.path.join(PYTHON_SCRIPT_DIR,fileName),'r')
    data = ''
    for i in obj:
        data += i
    return data

def readFile(path,method='rb'):
    with open(path,method)as f:
        while True:
            data = f.read(BUFFSIZE)
            if not data:
                break
            else:
                yield data

def jsonLoad(path,encoding='utf-8'):
    if fileExists(path):
        obj = readFile(path,'r')
        data = ''
        for i in obj:
            data += i
        try:
            return json.loads(data,encoding=encoding)
        except Exception:
            return {}
    else:
        return {}

def jsonDumps(obj):
    return json.dumps(obj)


def scriptSpendTime(func,args=()):
    if type(args) != tuple:
        raise '必须是元组'
    else:
        start = time.clock()
        func(*args)
        end = time.clock()
        return end - start

def getFonts():
    fonts = getFiles(FONTS_DIR)
    dic = {}
    for font in fonts:
        _,fileFullName = os.path.split(font)
        fileName,extendName = os.path.splitext(fileFullName)
        dic[fileName] = os.path.join(FONTS,font)
    return dic

sys.path.append(PYTHON_SCRIPT_DIR)