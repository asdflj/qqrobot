import cqp
from mymain import *
import requests
import datetime
import base64


URL = r'https://mcapi.us/server/status?ip=www.laoyoutiaomc.fun'
PICPATH = cqp.returnPicPath()
PICNAME = r'serverFavicon.png'

@myMain
def main(g,q,m):
    try:
        response = requests.get(url=URL,timeout=5)
        content = response.json()
    except requests.exceptions.ConnectTimeout:
        return '返回超时，请稍后再重试!'
    except requests.exceptions.ReadTimeout:
        return '返回超时，请稍后再重试!'
    else:
        if not content.get('favicon',None):
            return '服务器已关闭'
        pic = decodeBase64Pic(content['favicon'])
        savePNG(pic)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        players = content['players']['now']
        if  players == 0:
            sendPic(PICNAME,'\n公告: %s \n幻想乡里现在一个人也没有哦！\n 请求在%s更新'%(content['motd'],now))
        else:
            sendPic(PICNAME,'\n公告: %s \n幻想乡里现在有 %s人，请求在%s更新'%(content['motd'],players,now))

def decodeBase64Pic(data):
    data = data.split(',')[-1]
    return base64.b64decode(data)

def savePNG(data):
    with open (PICPATH+PICNAME,'wb')as f:
        f.write(data)