# coding:utf-8

import logging
import random

import utils
import config


def validate(item, callback):
    http_url_pool = [
        "http://www.baidu.com",
        "http://cn.bing.com",
        "http://www.sohu.com",
        "http://www.sina.com.cn"
    ]
    https_url_pool = [
        "https://www.baidu.com",
        "https://www.zhihu.com"
    ]
    _type, _ip, _port = item.split(':')

    if _type == "http":
        url = random.choice(http_url_pool)
        proxies = {"http": "http://%s:%s" % (_ip, str(_port))}

    elif _type == "https":
        url = random.choice(https_url_pool)
        proxies = {"https": "http://%s:%s" % (_ip, str(_port))}

    elif _type == "socks5":
        url = random.choice(http_url_pool)
        proxies = {
            "http": "socks5://%s:%s" % (_ip, str(_port)),
            "https": "socks5://%s:%s" % (_ip, str(_port))
        }

    try:
        req = utils.send_http('get', url, timeout=config.timeout*3, proxies=proxies, allow_redirects=False)
        if req.ok:
            callback(item)
    except Exception, e:
        logging.error("Validate on %s Error: %s" % (item, str(e)))