from handler.middleware import BaseEventMiddleware
from handler.response import jsonResponse

class Main(BaseEventMiddleware):
    def process_request(self, content):
        raise Exception('a')
