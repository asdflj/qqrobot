import random
import requests
from mymain import *

URL = 'https://mc.meitangdehulu.com/message/query_domain?domain=%s&re=1&limit=%s'
TIPS = [
    '使用/name mod名字 来获取mod的详细信息',
    '注意特殊符号转义',
    '名字后面加参数limit=你要显示的数量',
    'mods显示上限为100'
]

@myMain
def main(g,q,m):
    if m.find('limit=') != -1 :
        name,limit = m.split('limit=')
    else:
        name = m
        limit = 10
    res = requests.get(url=URL%(name,limit)).json()
    if res['status'] == 'ok':
        if res['data'] == 'null':
            yield '未找到信息'
        else:
            yield 'mod版本:%s\nmod名字:\n%s\n当前显示上限为:%s'%(res['version'],'\n'.join(res['data']['names']),limit)
            yield random.choice(TIPS)
    else:
        yield '返回超时'

    