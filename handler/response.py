import re

from django.shortcuts import HttpResponse
import requests
from .settings import SERVER, COOLQ_ROBOT_ACCESS_TOKEN
import json

def jsonResponse(response,at=False):
    if not at:
        response['at_sender'] = False
    return HttpResponse(
        json.dumps(response),
        content_type='application/json'
    )

def asyncResponse(url,params):
    request(url=url, params=params)
    return returnNone()

def request(url,params):
    if COOLQ_ROBOT_ACCESS_TOKEN:
        requests.get(url=url,params=params,headers={'Authorization':'Token '+COOLQ_ROBOT_ACCESS_TOKEN})
    else:
        requests.get(url=url, params=params)

def groupResponse(content,text):
    params = messageType(content,text,'group')
    return asyncResponse(url=SERVER + '/send_msg', params=params)

def privateResponse(content,text):
    params = messageType(content,text,'private')
    return asyncResponse(url=SERVER + '/send_msg', params=params)

def discussResponse(content,text):
    params = messageType(content,text,'discuss')
    return asyncResponse(url=SERVER + '/send_msg', params=params)

def messageType(content,text,mType):
    if mType == 'group':
        return {'message_type':mType,'message':text,'group_id':content['group_id']}
    elif mType == 'private':
        return {'message_type': mType, 'message': text, 'user_id': content['user_id']}
    elif mType == 'discuss':
        return {'message_type': mType, 'message': text, 'discuss_id': content['discuss_id']}

def returnNone(*args,**kwargs):
    return HttpResponse('')

def command(pattern,fnc,field):
    class Fn:
        def __init__(self,pattern,fnc,field):
            self._patternText = pattern
            self._pattern = re.compile(pattern)
            self._func = fnc
            self._field = field

        def getFunction(self):
            return self._func
        def getField(self):
            return self._field
        def getPattern(self):
            return self._pattern

        def getPatternText(self):
            return self._patternText

        def matchPattern(self,request):
            if self.getPattern().search(request[self.getField()]):
                return True
            else:
                return False

        def run(self,request):
            return self.getFunction()(request)

    return Fn(pattern,fnc,field)