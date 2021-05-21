# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import DatabaseError
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.manager import EmptyManager
from django.contrib.auth.models import Group, Permission
from django.utils.functional import cached_property
from django.utils.encoding import force_str

from . import cache


class ModelChangeMixin(object):
    '''Monitor the changed attributes'''

    def __setattr__(self, name, value):
        if not name.startswith('_') and name in self.__dict__:
            self._to_change(name, value)
        object.__setattr__(self, name, value)

    def _to_change(self, name, value):
        if name not in self.changed_map:
            self.changed_map[name] = getattr(self, name, None)
        if value == self.changed_map[name]:
            del self.changed_map[name]

    @cached_property
    def changed_map(self):
        return {}

    def get_origin(self, name):
        return self.changed_map.get(name, getattr(self, name))


class ModelFieldChangeMixin(ModelChangeMixin):
    '''Monitor the changed fields

    NOTE: DOT NOT USE `get_origin` to find the origin
    related object when you are not sure it was cached
    because the rel field would not be kept in
    `changed_map` when its data did not load
    from DB after set it to a new object.
    '''

    def __setattr__(self, name, value):
        if not name.startswith('_') and name in self.__dict__:
            if not hasattr(self._meta, '_attname_map'):
                _attname_map = {}
                _name_map = {}
                _auto_now_names = set()
                cache = self._meta._get_fields(reverse=False, include_hidden=True)
                for field in cache:
                    # model fields defined directly and not primary key
                    if isinstance(field, models.Field) and not field.primary_key:
                        _attname_map[field.attname] = field
                        _name_map[field.name] = field
                        if isinstance(field, models.DateField) and field.auto_now:
                            _auto_now_names.add(field.name)

                self._meta._attname_map = _attname_map
                self._meta._name_map = _name_map
                self._meta._auto_now_names = _auto_now_names
            if name in self._meta._attname_map:
                field = self._meta._attname_map.get(name)
                self._to_change(name, value)
                # push only to prevent from these multiple related field
                # such as generic.GenericForeignKey
                self.changed_fields.add(field.name)
            # check the cached related objects into changed map
            elif name in self._meta._name_map:
                field = self._meta._name_map.get(name)
                # ForeignKey or OneToOneField
                if isinstance(field, models.ForeignKey):
                    # whether the data loaded from DB
                    # NOTE: DOT NOT USE `get_origin` to find the origin
                    # related object when you are not sure it was cached
                    # because the rel field would not be kept in
                    # `changed_map` when its data did not load
                    # from DB after set it to a new Model object.
                    if (name in self.__dict__ or getattr(self, field.attname) is None):
                        self._to_change(name, value)
                else:
                    self._to_change(name, value)

        object.__setattr__(self, name, value)

    @cached_property
    def changed_fields(self):
        return set()

    def save_changed(self, using=None):
        '''save the changed fields'''
        if self.changed_fields:
            self.changed_fields.update(getattr(self._meta, '_auto_now_names', set()))
            self.save(force_update=True, update_fields=list(self.changed_fields), using=using)
            self.changed_fields.clear()
            self.changed_map.clear()


class BaseModel(models.Model, ModelFieldChangeMixin):

    _MODEL_WITH_CACHE = True
    _MODEL_CACHE_TTL = 600

    class Meta:
        abstract = True
        ordering = ['-pk', ]

    @classmethod
    def _prepare(cls):
        if 'edit' not in cls._meta.default_permissions:
            cls._meta.default_permissions += ('edit',)
        ModelBase._prepare(cls)

    @classmethod
    def autocomplete_search_fields(cls):

        if hasattr(cls, '_autocomplete_search_fields'):
            return cls._autocomplete_search_fields

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name
        return ['pk__iexact', ] + [construct_search(str(search_field)) for search_field in cls.search_fields()]

    @classmethod
    def search_fields(cls):
        if hasattr(cls, '_search_fields'):
            return cls._search_fields
        ret = set()
        for field in cls._meta.fields:
            if not field.db_index and not field.unique:
                continue
            if isinstance(field, models.ForeignKey) or isinstance(field, models.ManyToManyField):
                continue
            if isinstance(field, models.CharField):
                ret.add('^%s' % field.name)
            elif isinstance(field, models.IntegerField) and not field.choices:
                ret.add('=%s' % field.name)
        cls._search_fields = ret
        return ret

    @classmethod
    def get_child_field(cls, attr):
        field_names = attr.split('__')
        head_model = cls
        name = ''
        field = None
        for field_name in field_names:
            if head_model is None:
                raise RuntimeError('{} not found {}'.format(cls, attr))
            field = head_model._meta.get_field(field_name)
            head_model = field.remote_field.model if field.remote_field is not None else None
            if name == '':
                name = field.verbose_name
            else:
                name += ' ' + field.verbose_name
        return isinstance(field, models.BooleanField), name

    def __str__(self):
        return force_str('%s%s(%d)' % (self.__class__.__name__, self._meta.verbose_name, self.pk))

    def __unicode__(self):
        return '%s%s(%d)' % (self.__class__.__name__, self._meta.verbose_name, self.pk)

    @classmethod
    def get_obj_by_pk_from_cache(cls, pk):
        if cls._MODEL_WITH_CACHE:
            return cache.ModelPkCache.get(cls, pk)
        else:
            return cls.objects.filter(pk=pk).first()

    @classmethod
    def flush_cache_by_pk(cls, pk):
        if cls._MODEL_WITH_CACHE and pk is not None:
            cache.ModelPkCache.delete(cls, pk)

    @classmethod
    def get_obj_by_unique_key_from_cache(cls, **kwargs):
        assert len(kwargs) == 1
        key, value = list(kwargs.items())[0]
        if cls._MODEL_WITH_CACHE:
            return cache.ModelUniqueFieldCache.get(cls, key, value)
        else:
            return cls.objects.filter(**{key: value}).first()

    @classmethod
    def flush_cache_by_unique_key(cls, **kwargs):
        assert len(kwargs) == 1
        key, value = list(kwargs.items())[0]
        if cls._MODEL_WITH_CACHE and value is not None:
            cache.ModelUniqueFieldCache.delete(cls, key, value)

    def flush_cache(self):
        self.flush_cache_by_pk(self.pk)
        for field in self._meta.fields:
            if field.unique:
                self.flush_cache_by_unique_key(**field.get_filter_kwargs_for_object(self))

    def delete(self, using=None, keep_parents=False):
        self.flush_cache()
        return super(BaseModel, self).delete(using=using, keep_parents=keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.flush_cache()
        if not (force_insert or force_update or update_fields):
            if self._meta.select_on_save:
                pk_val = self._meta.model.objects.filter(pk=self.pk).values_list('pk', flat=True).first()
                if pk_val is None:
                    force_insert = True
                else:
                    force_update = True

        if update_fields:
            fd = [f.name for f in self._meta.fields]

            for f in update_fields:
                if f not in fd:
                    update_fields.remove(f)
        try:
            super(BaseModel, self).save(force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields)
        except DatabaseError as exp:
            if str(exp).endswith('did not affect any rows.'):
                pass
            else:
                raise


class AbstractUserMixin(object):
    is_staff = False
    is_active = True
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def _get_groups(self):
        return self._groups
    groups = property(_get_groups)

    def _get_user_permissions(self):
        return self._user_permissions
    user_permissions = property(_get_user_permissions)

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False

    def get_username(self):
        return ''
