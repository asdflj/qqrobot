from handler import response
from handler.middleware import BaseEventMiddleware


class Main(BaseEventMiddleware):
    def process_request(self,content):
        if content['notice_type'] == 'group_increase' and content['group_id'] in [873931242,630943368,566191243]:
            return response.groupResponse(content,'aaa')