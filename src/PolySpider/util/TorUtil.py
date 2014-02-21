import os
from config import Config

'''
目前Tor无法直接连接Configuration Server导致无法获取P2P的节点信息，需要配置类似goAgent之类的代理服务器才能使用
目前暂时不实现，会在v0.5版本中实现利用Tor进行匿名和rotatedIp方面的工作
'''
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = Config.get('HTTP_PROXY')