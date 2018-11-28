from django.shortcuts import render,HttpResponse
from handler.response import returnNone
from .settings import CORE_MIDDLEWARE,EVENT_MIDDLEWARE,MESSAGE_TYPE
from .middleware import Middleware
from .event.event_patterns import eventPatterns
# Create your views here.



def handler(request):
    # 执行中间件
    mid = Middleware(request,CORE_MIDDLEWARE)
    # 执行函数
    return mid.execute(main)

def exec(request,messageType):
    # 先执行中间件，消息处理，再中间件
    mid = Middleware(request.POST, EVENT_MIDDLEWARE[messageType])
    for e in eventPatterns:
        if e.matchPattern(request.POST):
            return mid.execute(e.getFunction())
    else:
        return mid.execute(returnNone)

def main(request):
    # 匹配事件
    print(request.POST)
    if request.POST['post_type'] == MESSAGE_TYPE['MESSAGE']:
        return exec(request,MESSAGE_TYPE['MESSAGE'])
    elif request.POST['post_type'] == 'notice':
        return exec(request, MESSAGE_TYPE['NOTICE'])
    elif request.POST['post_type'] == 'request':
        return exec(request, MESSAGE_TYPE['REQUEST'])
    elif request.POST['post_type'] == 'meta_event':
        return exec(request, MESSAGE_TYPE['META_EVENT'])
    return returnNone()

