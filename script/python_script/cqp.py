import requests

URL = 'http://192.168.1.114:5700'

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

# def returnPicPath():
#     return IMAGES_DIR +'/'
#
# def returnFonts():
#     return getFonts()

