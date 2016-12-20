#coding:utf-8

from utils import send_http, getHtmlTree, robustFunc
from service import PROXY_SEP, PROXY_TYPES


class kuaidaili(object):
    def __init__(self):
        self.items = []  # type:ip:port

    @robustFunc
    def run(self):
        urls = ["http://www.kuaidaili.com/proxylist/%d/" % i for i in xrange(1, 11)]
        for url in urls:
            req = send_http('get', url)
            tree = getHtmlTree(req.content)
            proxy_list = tree.xpath('.//tbody/tr')
            for proxy in proxy_list:
                ip = proxy.xpath('.//td[@data-title="IP"]/text()')[0]
                port = proxy.xpath('.//td[@data-title="PORT"]/text()')[0]
                _tmp_ptypes = proxy.xpath('.//td[@data-title="%s"]/text()' % u"类型")[0]
                ptypes = map(lambda _: _.strip().lower(), _tmp_ptypes.split(','))
                for ptype in ptypes:
                    if ptype in PROXY_TYPES:
                        self.items.append(ptype + PROXY_SEP + ip + ':' + str(port))