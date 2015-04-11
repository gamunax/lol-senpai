__author__ = 'Dewep'

from flask import g
import redis
from settings import REDIS_URL


def get_db():
    try:
        db = getattr(g, '_database', None)
    except RuntimeError:
        db = None
    if db is None:
        db = redis.from_url(REDIS_URL)
        try:
            g._database = db
        except RuntimeError:
            pass
    return db


class Cache(object):
    @staticmethod
    def set(name, value, ex=None, px=None, nx=False, xx=False):
        return get_db().set(name, value, ex, px, nx, xx)

    @staticmethod
    def get(name):
        return get_db().get(name)
