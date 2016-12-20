# coding:utf-8

import redis
from utils import singletonCls


@singletonCls
class RedisClient(object):
    def __init__(self, config):
        self.r = redis.Redis(host=config['DB_Host'], port=config['DB_Port'], db=config['DB_Name'], password=config['DB_Passwd'])

    def add(self, k, v):
        return self.r.sadd(k, v)

    def get(self, k, n):
        return self.r.srandmember(k, n)

    def pop(self, k):
        return self.r.spop(k)

    def delRecord(self, k, v):
        return self.r.srem(k, v)

    def delTable(self, k):
        return self.r.delete(k)

    def len(self, k):
        return self.r.scard(k)