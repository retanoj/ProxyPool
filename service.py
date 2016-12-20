# coding:utf-8

from gevent import monkey
monkey.patch_all()

import gevent
import logging

from DB.RedisClient import RedisClient
from config import DB_Config, Crawlers
from validator import validate

PROXY = 'proxy:'
PROXY_TYPES = ['http', 'https', 'socks5']
UNCHECK = PROXY + 'uncheck'
CHECKED = PROXY + 'checked'
PROXY_SEP = ':'


class ProxyService(object):
    def __init__(self):
        self.r = RedisClient(DB_Config)

    def get(self, ptype, n=1):
        n = 10 if n > 10 else n
        ptype = ptype.lower()
        if ptype in PROXY_TYPES:
            return self.r.get(PROXY + ptype, n)
        return []

    def delete(self, ptype, v):
        ptype = ptype.lower()
        if ptype in PROXY_TYPES:
            return self.r.delRecord(PROXY + ptype, v)

    def refresh(self):
        self.__fetch()
        self.__validate()
        self.__flush()
        return 'ok'

    def __fetch(self):
        """ feed proxy:uncheck set """

        for _cr in Crawlers:
            _crpath = '.'.join(['ProxyCrawler', _cr])
            logging.info("import crawler: %s" % _crpath)
            Crawler = getattr(__import__(_crpath, fromlist=[_cr]), _cr)
            crawler = Crawler()
            crawler.run()
            for item in crawler.items:
                self.r.add(UNCHECK, item)

    def __validate(self):
        """ proxy:uncheck set -> proxy:checked set """

        def __callback(item):
            self.r.add(CHECKED, item)

        total = self.r.len(UNCHECK)
        logging.info("need to validate %d proxies" % total)
        limit = 1000
        for offset in xrange(0, total, limit):
            events = []
            for _ in xrange(limit):
                item = self.r.pop(UNCHECK)
                if not item: break
                events.append(gevent.spawn(validate, item, __callback))
            gevent.joinall(events)

    def __flush(self):
        """ proxy:checked set -> proxy:{http, https, socks5} set """

        # clean all
        for _type in PROXY_TYPES:
            self.r.delTable(PROXY + _type)

        item = self.r.pop(CHECKED)
        while item:
            prefix, proxy = item.split(PROXY_SEP, 1)
            self.r.add(PROXY + prefix, proxy)
            item = self.r.pop(CHECKED)
