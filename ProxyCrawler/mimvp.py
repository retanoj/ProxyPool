# coding:utf-8

import pytesseract
import StringIO
from PIL import Image
from utils import send_http, getHtmlTree, robustFunc
from service import PROXY_SEP, PROXY_TYPES


class mimvp(object):
    def __init__(self):
        self.items = [] # type:ip:port
        self.cache = {} # img_key: port

    @robustFunc
    def run(self):
        urls = ["http://proxy.mimvp.com/free.php?proxy=in_hp&sort=&page=1",
                "http://proxy.mimvp.com/free.php?proxy=out_tp&sort=&page=1",
                "http://proxy.mimvp.com/free.php?proxy=out_hp&sort=&page=1",
                "http://proxy.mimvp.com/free.php?proxy=in_socks&sort=&page=1",
                "http://proxy.mimvp.com/free.php?proxy=out_socks&sort=&page=1"]
        for url in urls:
            req = send_http('get', url)
            tree = getHtmlTree(req.content)
            _proxy_list = tree.xpath('.//tbody/td')
            proxy_list = [_proxy_list[i:i+10] for i in xrange(0, len(_proxy_list), 10)]
            for proxy in proxy_list:
                ip = proxy[1].text
                port = self.numocr("http://proxy.mimvp.com/" + proxy[2][0].attrib['src'])
                _tmp_ptype = proxy[3].text
                ptypes = map(lambda _: _.strip().lower(), _tmp_ptype.split('/'))
                for ptype in ptypes:
                    if ptype in PROXY_TYPES:
                        self.items.append(ptype + PROXY_SEP + ip + ':' + str(port))

    def numocr(self, url):
        '''
        图像识别不保证100%准确
        经测试, 3128 -> 3328 , 137 -> 337
        '''

        key = url.split('port=')[-1]
        if key in self.cache:
            return self.cache.get(key)

        img = send_http('get', url).content
        img = Image.open(StringIO.StringIO(img))

        port = pytesseract.image_to_string(img, lang='osd', config="digits")
        self.cache[key] = port
        return port