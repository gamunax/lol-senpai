__author__ = 'Dewep'

from flask import g
import redis
from settings import REDIS_URL


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = redis.from_url(REDIS_URL)
    return db


class Cache(object):
    @staticmethod
    def set(name, value, ex=None, px=None, nx=False, xx=False):
        return get_db().set(name, value, ex, px, nx, xx)

    @staticmethod
    def get(name):
        return get_db().get(name)
