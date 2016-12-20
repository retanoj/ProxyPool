# coding:utf-8

from utils import send_http, getHtmlTree, robustFunc
from service import PROXY_SEP, PROXY_TYPES


class goubanjia(object):
    def __init__(self):
        self.items = []  # type:ip:port

    @robustFunc
    def run(self):
        urls = ["http://www.goubanjia.com/free/gngn/index.shtml",
                "http://www.goubanjia.com/free/gnpt/index.shtml",
                "http://www.goubanjia.com/free/gwgn/index.shtml",
                "http://www.goubanjia.com/free/gwpt/index.shtml"]
        for url in urls:
            req = send_http('get', url)
            tree = getHtmlTree(req.content)
            proxy_list = tree.xpath('.//td[@class="ip"]')
            for proxy in proxy_list:
                _tmp_proxy = proxy.xpath('.//*[not(contains(@style, "none"))]/text()')
                ip, port = ''.join(_tmp_proxy[:-1]), _tmp_proxy[-1]
                _tmp_ptype = proxy.xpath('../td[3]/a/text()')[0]
                ptypes = map(lambda _: _.strip().lower(), _tmp_ptype.split(','))
                for ptype in ptypes:
                    if ptype in PROXY_TYPES:
                        self.items.append(ptype + PROXY_SEP + ip + ':' + str(port))
