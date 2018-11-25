import requests
from handler.util import IMAGES_DIR, getFonts
from handler.settings import SERVER
URL = SERVER

def sendGroupMsg(g,text):
    requests.get(URL+'/send_group_msg',params={
        'group_id':g,
        'message':text,
    })

def sendPrivateMsg(q,text):
    requests.get(URL+'/send_private_msg',params={
        'user_id':q,
        'message':text,
    })

def returnPicPath():
    return IMAGES_DIR +'/'

def returnFonts():
    return getFonts()