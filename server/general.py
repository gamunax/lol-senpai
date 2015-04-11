__author__ = 'Dewep'

from flask import g
from settings import REDIS_URL, API_KEY, LOG_LEVEL


_local_cache = dict()


def _cache_instance_flask(_id, new):
    _id = '_' + _id
    try:
        instance = getattr(g, _id, None)
    except RuntimeError:
        instance = _local_cache[_id] if _id in _local_cache else None
    if instance is None:
        instance = new()
        try:
            setattr(g, _id, instance)
        except RuntimeError:
            _local_cache[_id] = instance
    return instance


def get_wrapper():
    from library.api.league_of_legends import LeagueOfLegends
    return _cache_instance_flask('wrapper', lambda: LeagueOfLegends(API_KEY))


def get_db():
    import redis
    return _cache_instance_flask('database', lambda: redis.from_url(REDIS_URL))


def get_logger():
    def new():
        import logging
        logger = logging.getLogger('Log-Senpai')
        logger.setLevel(logging.INFO)
        if LOG_LEVEL in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
            logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        formatter = logging.Formatter('\033[34;1m [%(asctime)s] [%(levelname)s]  %(message)s\033[0m')
        stream = logging.StreamHandler()
        stream.setLevel(logger.level)
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger
    return _cache_instance_flask('logging', lambda: new())


log = get_logger()


def function_logger(function):
    def case_decorator(*args, **kwargs):
        info = "CallFunction:  %s(" % function.__name__
        for arg in args:
            info += "%s, " % arg
        for key, value in kwargs:
            info += "%s=%s, " % (key, value)
        log.info(info + ")")
        ret = function(*args, **kwargs)
        log.debug("Result %s: %s" % (function.__name__, ret))
        return ret
    return case_decorator


class Cache(object):
    @staticmethod
    def set(name, value, ex=None, px=None, nx=False, xx=False):
        return get_db().set(name, value, ex, px, nx, xx)

    @staticmethod
    def get(name):
        return get_db().get(name)
