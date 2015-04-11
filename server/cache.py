__author__ = 'Dewep'

from flask import g
import redis
from settings import REDIS_URL, API_KEY


def _cache_instance_flask(_id, new):
    _id = '_' + _id
    try:
        instance = getattr(g, _id, None)
    except RuntimeError:
        instance = None
    if instance is None:
        instance = new()
        try:
            setattr(g, _id, instance)
        except RuntimeError:
            pass
    return instance


def get_wrapper():
    from library.api.league_of_legends import LeagueOfLegends
    return _cache_instance_flask('wrapper', lambda: LeagueOfLegends(API_KEY))


def get_db():
    return _cache_instance_flask('database', lambda: redis.from_url(REDIS_URL))


class Cache(object):
    @staticmethod
    def set(name, value, ex=None, px=None, nx=False, xx=False):
        return get_db().set(name, value, ex, px, nx, xx)

    @staticmethod
    def get(name):
        return get_db().get(name)
