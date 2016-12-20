# coding:utf-8

import logging
import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import config


def singletonCls(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


def robustFunc(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(str(e))

    return decorate


def getHtmlTree(html):
    return etree.HTML(html)


def send_http(method, url, headers={}, payload={}, timeout=config.timeout, *args, **kwargs):
    fake_headers = config.fake_headers.copy()
    fake_headers.update(headers)
    func = getattr(requests, method, 'head')
    if method == 'get' or method == 'head':
        return func(url, headers=fake_headers, timeout=timeout, verify=False, *args, **kwargs)
    elif method == 'post':
        return func(url, headers=fake_headers, data=payload, timeout=timeout, verify=False, *args, **kwargs)
    return None
