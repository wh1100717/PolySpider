import os
from config import Config

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = Config.get('HTTP_PROXY')