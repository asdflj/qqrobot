import importlib
import traceback
class Middleware:
    def __init__(self,request,middleware):
        self.request = request
        self.middleware = middleware

    def execute(self,response):
        try:
            objects = self.initClass(response)
            for obj in objects:
                result = obj.process_request(self.getRequest())
                if result:
                    return result
            view_response = response(self.getRequest())
            for obj in objects[::-1]:
                result = obj.process_response(self.getRequest(),view_response)
                if result:
                    return result
            else:
                return view_response
        except Exception as e:
            for obj in self.initClass(response):
                result = obj.process_exception(traceback.format_exc())
                if result:
                    return result

    def getRequest(self):
        return self.request

    def initClass(self,response):
        L = []
        for mid in self.middleware:
            m = self.split(mid)
            mod = importlib.import_module(m[0])
            cls = getattr(mod, m[1])
            obj = cls(response)
            L.append(obj)
        return L

    def split(self,moduleName):
        L = moduleName.split('.')
        filename = '.'.join(L[:-1])
        moduleClass = L[-1]
        return (filename,moduleClass)

class BaseMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
        super(BaseMiddleWare, self).__init__()

    def process_request(self,request):
        pass

    def process_exception(self,exception):
        pass

    def process_response(self, request, response):
        pass

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class BaseEventMiddleware(BaseMiddleWare):  
    def process_request(self,content):
        pass

    def process_exception(self,exception):
        raise Exception(exception)
        
    def process_response(self,content,response):
        pass

    def __str__(self):
        return None




