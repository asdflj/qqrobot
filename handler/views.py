from django.shortcuts import render,HttpResponse
from handler.response import returnNone
from .settings import CORE_MIDDLEWARE,EVENT_MIDDLEWARE
from .middleware import Middleware
from .event.event_patterns import eventPatterns
# Create your views here.

EVENT = [
    (0,'private'),
    (1,'group'),
    (2,'discuss'),
    (3,'group_upload'),
    (4,'group_admin'),
    (5,'group_decrease'),
    (6,'group_increase'),
    (7,'friend_add'),
    (8,'add_friend_request'),
    (9,'add_group_request'),
]

def handler(request):
    # 执行中间件
    mid = Middleware(request,CORE_MIDDLEWARE)
    # 执行函数
    return mid.execute(main)

def exec(request,messageType):
    mid = Middleware(request.POST, EVENT_MIDDLEWARE[messageType])
    for e in eventPatterns:
        if e.matchPattern():
            return mid.execute(e.getFunction())
    else:
        return mid.execute(returnNone)

def main(request):
    # 匹配事件
    print(request.POST)
    if request.POST['post_type'] == 'message':
        # 先执行中间件，消息处理，再中间件
        return exec(request,'message')
    elif request.POST['post_type'] == 'notice':
        return exec(request, 'notice')
    elif request.POST['post_type'] == 'request':
        return exec(request, 'request')
    elif request.POST['post_type'] == 'meta_event':
        return exec(request, 'meta_event')

    return returnNone()

