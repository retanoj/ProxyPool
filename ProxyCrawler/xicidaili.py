# coding:utf-8

from utils import send_http, getHtmlTree, robustFunc
from service import PROXY_SEP, PROXY_TYPES


class xicidaili(object):
    def __init__(self):
        self.items = []  # type:ip:port

    @robustFunc
    def run(self):
        urls = ["http://www.xicidaili.com/nn/1",
                "http://www.xicidaili.com/nn/2"]
        for url in urls:
            req = send_http('get', url)
            tree = getHtmlTree(req.content)
            proxy_list = tree.xpath('.//table[@id="ip_list"]/*')[1:]
            for proxy in proxy_list:
                ip = proxy.xpath('.//td[2]/text()')[0]
                port = proxy.xpath('.//td[3]/text()')[0]
                ptype = proxy.xpath('.//td[6]/text()')[0]
                if ptype in PROXY_TYPES:
                    self.items.append(ptype + PROXY_SEP + ip + ':' + str(port))