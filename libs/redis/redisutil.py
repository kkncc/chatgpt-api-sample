# -*- coding:utf-8 -*-
from apps import GLOBAL_REDIS_CLIENT


def hget(key, field):
    return GLOBAL_REDIS_CLIENT.hget(key.lower(), field)


def hset(key, field, val):
    return GLOBAL_REDIS_CLIENT.hset(key.lower(), field, val)


def hgetall(key):
    return GLOBAL_REDIS_CLIENT.hgetall(key.lower())


def hdel(key, field):
    return GLOBAL_REDIS_CLIENT.hdel(key.lower(), field)


def set(key, value, ex=None, px=None, nx=False, xx=False):
    return GLOBAL_REDIS_CLIENT.set(key.lower(), value, ex, px, nx, xx)


def get(key):
    return GLOBAL_REDIS_CLIENT.get(key.lower())


def delete(key):
    return GLOBAL_REDIS_CLIENT.delete(key.lower())


def hmset(name, mapper):
    return GLOBAL_REDIS_CLIENT.hmset(name, mapper)

