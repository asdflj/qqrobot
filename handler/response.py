from django.shortcuts import HttpResponse
import requests
from .settings import SERVER
import json

def jsonResponse(response,at=False):
    if not at:
        response['at_sender'] = False
    return HttpResponse(
        json.dumps(response),
        content_type='application/json'
    )

def asyncResponse(content,text,mType):
    params = messageType(content,text,mType)
    requests.get(url=SERVER + '/send_msg', params=params)
    return returnNone()

def groupResponse(content,text):
    params = messageType(content,text,'group')
    requests.get(url=SERVER + '/send_msg', params=params)
    return returnNone()

def privateResponse(content,text):
    params = messageType(content,text,'private')
    requests.get(url=SERVER + '/send_msg', params=params)
    return returnNone()

def discussResponse(content,text):
    params = messageType(content,text,'discuss')
    requests.get(url=SERVER + '/send_msg', params=params)
    return returnNone()

def messageType(content,text,mType):
    if mType == 'group':
        return {'message_type':mType,'message':text,'group_id':content['group_id']}
    elif mType == 'private':
        return {'message_type': mType, 'message': text, 'user_id': content['user_id']}
    elif mType == 'discuss':
        return {'message_type': mType, 'message': text, 'discuss_id': content['discuss_id']}

def returnNone(*args,**kwargs):
    return HttpResponse('')

def command(pattern,fnc):
    class Fn:
        def __init__(self,pattern,fnc):
            self._patternText = pattern
            self._pattern = re.compile(pattern)
            self._func = fnc

        def getFunction(self):
            return self._func

        def getPattern(self):
            return self._pattern

        def getPatternText(self):
            return self._patternText

        def matchPattern(self,text):
            if self.getPattern().search(text):
                return True
            else:
                return False

        def run(self,request):
            return self.getFunction()(request)

    return Fn(pattern,fnc)