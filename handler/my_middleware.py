from .middleware import BaseMiddleWare
from .response import returnNone,jsonResponse
import json
import hmac
from .settings import COOLQ_ROBOT_SECRET,COOLQ_ROBOT_ACCESS_TOKEN,MESSAGE_TYPE
from handler.util import translate
class RequestMethod(BaseMiddleWare):
    def process_request(self,request):
        if not request.method == 'POST':
            return returnNone()

class Transjson(BaseMiddleWare):
    def process_request(self,request):
        if request.body:
            try:
                request.POST = json.loads(request.body.decode())
            except Exception:
                return returnNone()
        else:
            return returnNone()

class HMAC_Signature(BaseMiddleWare):
    def process_request(self,request):
        if request.body:
            try:
                if COOLQ_ROBOT_SECRET:
                    sig = hmac.new(COOLQ_ROBOT_SECRET.encode(), request.body, 'sha1').hexdigest()
                    # print(request.META)
                    received_sig = request.META['HTTP_X_SIGNATURE'][len('sha1='):]
                    if sig == received_sig:
                        # 请求确实来自于插件
                        pass
                    else:
                        # 假的上报
                        return returnNone()
            except Exception as e:
                print(e)
                return returnNone()
        else:
            return returnNone()

class Escape(BaseMiddleWare):
    def process_request(self,request):
        if request.body and request.POST.get(MESSAGE_TYPE['MESSAGE'],None):
            request.POST[MESSAGE_TYPE['MESSAGE']] = translate(request.POST[MESSAGE_TYPE['MESSAGE']])