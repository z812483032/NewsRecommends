# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.core.cache import cache
from django.utils.encoding import force_text


class BaseCacheItem(object):
    _prefix = None
    _expire_secs = 3600 * 24

    @classmethod
    def get_prefix(cls):
        return cls._prefix

    @classmethod
    def _getkey(cls, key):
        assert cls.get_prefix() is not None
        return 'cache:%s:%s' % (cls._prefix, force_text(key))

    @classmethod
    def add(cls, key, value, timeout=None):
        if timeout is None:
            timeout = cls._expire_secs
        return cache.add(cls._getkey(key), value, timeout)

    @classmethod
    def get(cls, key, default=None):
        return cache.get(cls._getkey(key), default)

    @classmethod
    def set(cls, key, value, timeout=None):
        if timeout is None:
            timeout = cls._expire_secs
        return cache.set(cls._getkey(key), value, timeout)

    @classmethod
    def delete(cls, key):
        return cache.delete(cls._getkey(key))

    @classmethod
    def incr(cls, key, delta=1):
        if cls.get(key) is None:
            cls.set(key, 0)
        return cache.incr(cls._getkey(key), delta)

    @classmethod
    def has_key(cls, key):
        return cache.has_key(cls._getkey(key))  # NOQA

    @classmethod
    def ttl(cls, key):
        return cache.ttl(cls._getkey(key))

    @classmethod
    def get_or_set(cls, key, func, timeout=None):
        if timeout is None:
            timeout = cls._expire_secs
        return cache.get_or_set(cls._getkey(key), func, timeout)

    @classmethod
    def expire(cls, key, timeout):
        return cache.expire(cls._getkey(key), timeout)

    @classmethod
    def persist(cls, key):
        return cache.persist(cls._getkey(key))

    @classmethod
    def clear(cls):
        """只支持redis_cache"""
        return cache.delete_pattern(cls._getkey('*'))


class AdminFuncCache(BaseCacheItem):
    _prefix = None
    _expire_secs = 3600 * 24


class ModelCacheItem(BaseCacheItem):
    _prefix = 'apiview:model_cache'
    _expire_secs = 600


class ModelUniqueFieldCache(object):

    @classmethod
    def _getkey(cls, modelcls, field_name, field_key):
        assert field_key is not None
        assert issubclass(modelcls, models.Model)
        filed = modelcls._meta.get_field(field_name)
        assert filed.unique
        return "%s:%s:%s" % (modelcls._meta.db_table, filed.name, field_key)

    @classmethod
    def get(cls, modelcls, field_name, field_key):
        ret = ModelCacheItem.get(cls._getkey(modelcls, field_name, field_key))
        if ret is None:
            ret = modelcls.objects.filter(**{field_name: field_key}).first()
            if ret is not None:
                ttl = getattr(modelcls, '_MODEL_CACHE_TTL', None)
                ModelCacheItem.set(cls._getkey(modelcls, field_name, field_key), ret, ttl)
        return ret

    @classmethod
    def delete(cls, modelcls, filed_name, filed_key):
        return ModelCacheItem.delete(cls._getkey(modelcls, filed_name, filed_key))


class ModelPkCache(object):

    @classmethod
    def _getkey(cls, modelcls, pk):
        assert issubclass(modelcls, models.Model)
        return "%s:%s" % (modelcls._meta.db_table, pk)

    @classmethod
    def get(cls, modelcls, pk):
        ret = ModelCacheItem.get(cls._getkey(modelcls, pk))
        if ret is None:
            ret = modelcls.objects.filter(pk=pk).first()
            if ret is not None:
                ttl = getattr(modelcls, '_MODEL_CACHE_TTL', None)
                ModelCacheItem.set(cls._getkey(modelcls, pk), ret, ttl)
        return ret

    @classmethod
    def delete(cls, modelcls, pk):
        return ModelCacheItem.delete(cls._getkey(modelcls, pk))
