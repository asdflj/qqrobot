import cqp
from mymain import *
import requests
import datetime

URL='https://mcapi.us/server/status'


class Parse:
    def __init__(self,server):
        L=server.split(':')
        self.host=L[0]
        if len(L) ==2:
            self.port =int(L[1])
        else:
            self.port = 25565

@myMain
def main(g,q,m):
    obj =Parse(m)
    try:
        response = requests.get(url=URL,timeout=5,params={'ip':obj.host,'port':obj.port})
        content = response.json()
    except requests.exceptions.ConnectTimeout:
        return '返回超时，请稍后再重试!'
    except requests.exceptions.ReadTimeout:
        return '返回超时，请稍后再重试!'
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        players = content['players']['now']
        if  players == 0:
            return ('公告: %s \n服里现在一个人也没有哦！\n 请求在%s更新'%(content['motd'],now))
        else:
            return ('公告: %s \n服里现在有 %s人，请求在%s更新'%(content['motd'],players,now))