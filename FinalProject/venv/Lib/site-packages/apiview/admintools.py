# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import six
import copy
import mimetypes
from functools import wraps, reduce


from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import flatten_fieldsets, unquote
from django.contrib.admin.views import main
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError, FieldDoesNotExist
from django.core.validators import EMPTY_VALUES
from django.db import models, DJANGO_VERSION_PICKLE_KEY
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields.related import RelatedField
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.forms.models import modelform_factory, BaseModelFormSet, BaseInlineFormSet
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils.version import get_version
from import_export.admin import (
    ExportMixin as _ExportMixin,
    ImportMixin as _ImportMixin,
    ImportExportMixin as _ImportExportMixin,
)
from import_export.resources import ModelDeclarativeMetaclass, ModelResource

from apiview import mailtools, widgets

FIX_COLUMN_VAR = 'fc'
main.IGNORED_PARAMS += (FIX_COLUMN_VAR,)


def set_cache(method, mask, result):
    '''设置方法结果缓存'''
    if hasattr(method, 'im_self'):
        instance = method.im_self
        method_cache = getattr(instance, '_method_cache_', {})
        cache = method_cache.get(method.__name__, {})
        cache['mask'] = mask
        cache['result'] = result
        method_cache[method.__name__] = cache
        instance._method_cache_ = method_cache
    else:
        setattr(method, '_mask_', mask)
        setattr(method, '_result_', result)
        # method._mask_ = mask
        # method._result_ = result


def get_cache(method, mask, default=None):
    '''获取方法结果缓存，在识别码变更时清除缓存'''
    if hasattr(method, 'im_self'):
        instance = method.im_self
        method_cache = getattr(instance, '_method_cache_', {})
        cache = method_cache.get(method.__name__, {})
        if cache.get('mask', None) == mask:
            return cache.get('result', default)
        method_cache.pop(method.__name__, None)
    elif hasattr(method, '_mask_'):
        if method._mask_ == mask:
            return method._result_
        del method._mask_
        del method._result_
    return default


def get_mask(*args):
    return map(id, args)


def get_normal_fields(model):
    fields = []
    for field in model._meta.concrete_fields:
        if not (field.primary_key
                or isinstance(field, RelatedField)
                or isinstance(field, models.FileField)
                or field.name.startswith('_')):
            fields.append(field)
    return fields


class BaseModelResource(ModelResource):
    '''
    Use fields' verbose names as column names
    '''

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        field = super(BaseModelResource, cls).field_from_django_field(
            field_name, django_field, readonly
        )
        if field:
            field.column_name = django_field.verbose_name
        return field

    def export(self, queryset=None):

        import tablib
        """
        Exports a resource.
        """
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)

        if isinstance(queryset, QuerySet):
            if queryset._prefetch_related_lookups:
                # Could not enjoy the 'prefetch_related' method's benefits when
                # using 'iterator' to generate data
                iterable = iter(queryset)
            else:
                # Iterate without the queryset cache, to avoid wasting memory
                # when exporting large datasets.
                iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            data.append(self.export_resource(obj))
        return data


def modelresource_factory(model, resource_class=BaseModelResource):
    meta = copy.copy(resource_class._meta)
    meta.model = model
    class_name = model.__name__ + str('Resource')
    class_attrs = {'Meta': meta, }
    return ModelDeclarativeMetaclass(class_name, (resource_class,), class_attrs)


def extend_admincls(*admin_classes):
    assert (admin_classes)
    return type(b'_Admin', admin_classes, {})


def get_widget(field):
    if isinstance(field, models.ImageField):
        return widgets.ImageWidget
    return widgets.TagWidget


def get_fieldwidget(field):
    if isinstance(field, models.ImageField):
        return widgets.ImageFieldWidget
    return widgets.FieldWidget


def _lookup_field(name, obj):
    splices = name.split(LOOKUP_SEP)
    field_name = splices[-1]
    for gen in splices[:-1]:
        obj = getattr(obj, gen)

    field = obj._meta.get_field(field_name)
    if isinstance(field_name, RelatedField):
        label = field.remote_field.field.verbose_name
    else:
        label = field.verbose_name

    return field, label, getattr(obj, field.attname)


def format_field(verbose, field, options=None, **kwargs):
    '''
    Format field with given widgets or default

    Example:
        class MyAdminClass(models.ModelAdmin):
            list_display = [format_field(
                verbose='名字', field='username', options={
                    'style': 'color:red'
                }), ...]
    '''
    name = field
    widget_opts = options or {}

    def _format_field(obj):
        field, label, value = _lookup_field(name, obj)
        attrs = widget_opts.copy()
        widgetclass = attrs.pop('widgetclass', None)
        if widgetclass is None:
            widgetclass = get_widget(field)
        widget = widgetclass(attrs)
        return widget.render(label, value, {})

    _format_field.short_description = verbose
    _format_field.allow_tags = True
    for att, val in kwargs.items():
        setattr(_format_field, att, val)
    return _format_field


def collapse_fields(verbose, fields, options=None, **kwargs):
    '''
    Collapse_fields into one field in changelist_view in modeladmin site

    Example:
        class MyAdminClass(models.ModelAdmin):
            list_display = [collapse_fields(
                verbose='名字', fields=('username', 'name'), options={
                    'username':{'style': 'color:red'}
                }), ...]
    '''
    widget_map = {}
    for name in fields:
        if options:
            widget_kwargs = options.get(name, {})
            widgetclass = widget_kwargs.pop('widgetclass', None)
            widget_map[name] = {
                'widgetclass': widgetclass,
                'attrs': widget_kwargs,
            }
        else:
            widget_map[name] = {}

    def format_fields(obj):
        html = []
        for name in fields:
            field, label, value = _lookup_field(name, obj)
            widgetclass = widget_map[name].get('widgetclass', None) or get_fieldwidget(field)
            widget = widgetclass(widget_map[name].get('attrs', {}))
            html.append(widget.render(name, (label, value), None))
        return ''.join(html)

    format_fields.short_description = verbose
    format_fields.allow_tags = True
    for att, val in kwargs.items():
        setattr(format_fields, att, val)
    return format_fields


def limit_queryset(limits=None, base=QuerySet):
    '''
    return LimitQuerySet to set max rows and count returned by Database
    '''

    class LimitQuerySet(LimitQuerySetMixin, base):
        LIMIT = limits

    return LimitQuerySet


def get_related_model_fields(model, rel, is_foreign_key):
    '''通过model下rel对象获取相关字段或关联属性'''
    # 多对多关联的REL对象本身不区分关系前后
    # 相关代理类做同样处理
    if is_foreign_key and rel.field.model._meta.concrete_model == model._meta.concrete_model:
        return rel.field, rel.get_related_field()
    return rel.get_related_field(), rel.field


class StrictModelFormSet(BaseModelFormSet):
    '''Add validation to ensure POST data is up to date
    '''
    def _existing_object(self, pk):
        if not hasattr(self, '_object_dict'):
            queryset = self.get_queryset()
            if self.data:   # 提交数据时
                pk_field = self.model._meta.pk
                pks = []
                for i in range(self.total_form_count()):
                    prefix = self.add_prefix(i)
                    pk_val = self.data.get('%s-%s' % (prefix, pk_field.name))
                    if pk_val is not None:
                        pks.append(pk_val)
                queryset = queryset.filter(pk__in=pk_val)
            self._object_dict = {o.pk: o for o in queryset}
        obj = self._object_dict.get(pk)
        if obj is None:
            obj = self.get_queryset().filter(pk=pk).first()
            self._object_dict[pk] = obj
        return obj

    def clean(self):
        super(StrictModelFormSet, self).clean()
        self.validate_queryset()

    def validate_queryset(self):
        pk = self.model._meta.pk
        to_python = pk.to_python
        rel = pk.remote_field
        while rel:
            related_field = rel.get_related_field()
            to_python = related_field.to_python
            rel = related_field.remote_field

        updated = False
        for form in self.forms:
            pk_data = form[pk.name].data
            if (pk_data not in EMPTY_VALUES
                    and form.instance.pk != to_python(pk_data)):
                updated = True
                break
        if updated:
            new_formset = self.__class__(
                prefix=self.prefix,
                queryset=self.queryset,
            )
            self.forms = new_formset.forms
            raise ValidationError('页面数据已经更新，请修改后重新保存')


class StrictInlineFormSet(BaseInlineFormSet):
    '''Add validation to ensure POST data is up to date
    '''
    def _existing_object(self, pk):
        if not hasattr(self, '_object_dict'):
            queryset = self.get_queryset()
            if self.data:   # 提交数据时
                pk_field = self.model._meta.pk
                pks = []
                for i in range(self.total_form_count()):
                    prefix = self.add_prefix(i)
                    pk_val = self.data.get('%s-%s' % (prefix, pk_field.name))
                    if pk_val is not None:
                        pks.append(pk_val)
                queryset = queryset.filter(pk__in=pk_val)
            self._object_dict = {o.pk: o for o in queryset}
        obj = self._object_dict.get(pk)
        if obj is None:
            obj = self.get_queryset().filter(pk=pk).first()
            self._object_dict[pk] = obj
        return obj

    def clean(self):
        super(StrictInlineFormSet, self).clean()
        self.validate_queryset()

    def validate_queryset(self):
        pk = self.model._meta.pk
        to_python = pk.to_python
        rel = pk.remote_field
        while rel:
            related_field = rel.get_related_field()
            to_python = related_field.to_python
            rel = related_field.remote_field

        updated = False
        for form in self.forms:
            pk_data = form[pk.name].data
            if (pk_data not in EMPTY_VALUES
                    and form.instance.pk != to_python(pk_data)):
                updated = True
                break
        if updated:
            new_formset = self.__class__(
                save_as_new=self.save_as_new,
                prefix=self.prefix,
                queryset=self.queryset,
            )
            self.forms = new_formset.forms
            raise ValidationError('页面数据已经更新，请修改后重新保存')


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(' <a href="%s" target="_blank">'
                          '<img src="%s" alt="%s" style="max-width: 500px; max-height: 1000px" /></a>' %
                          (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(''.join(output))


# 所有proxy中ModelAdmin的基类
class ProxyModelAdmin(admin.ModelAdmin):
    '''default Admin class used by proxy|real models
    '''

    # db_for_read = DEFAULT_DB_ALIAS
    # db_for_write = DEFAULT_DB_ALIAS

    # remove "__str__"
    list_display = []

    # Extend options to manage site
    # extend field exclude RelatedField and PrimaryKey fields into list_display
    extend_normal_fields = True
    exclude_list_display = []
    heads = []
    tails = []
    # extend LimitQuerySet
    limits = 100
    # manage Add/Change view
    addable = True
    editable = True
    changeable = True
    # manage Change view
    change_view_readonly_fields = []
    editable_fields = None

    # precision
    precision = 2

    # cache key serials set
    cache_serial = set()

    actions = ['_reset']

    formset = StrictModelFormSet

    def __getattr__(self, attr):
        if ('__' in attr
                and not attr.startswith('_')
                and not attr.endswith('_boolean')
                and not attr.endswith('_short_description')):

            def dyn_lookup(instance):
                # traverse all __ lookups
                return reduce(lambda parent, child: getattr(parent, child),
                              attr.split('__'),
                              instance)

            # get admin_order_field, boolean and short_description
            dyn_lookup.admin_order_field = attr
            dyn_lookup.boolean = getattr(self, '{}_boolean'.format(attr), False)
            dyn_lookup.short_description = getattr(
                self, '{}_short_description'.format(attr),
                attr.replace('_', ' ').capitalize())

            return dyn_lookup

        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)

    def _reset(self, request, querset):
        pass

    _reset.short_description = '清空选项'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.ImageField):
            kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ProxyModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_editable_fields(self, request, obj=None):
        if not self.editable:
            return ()
        if self.editable_fields == forms.ALL_FIELDS:
            return None
        elif self.editable_fields is None:
            return ()

        return self.editable_fields

    def get_queryset(self, request):
        '''extend LimitQuerySet to manage rows
        '''
        queryset = super(ProxyModelAdmin, self).get_queryset(request)

        if self.limits:
            klass = limit_queryset(self.limits, queryset.__class__)
            queryset = klass.from_queryset(queryset)

        if not self.has_delete_permission(request) and not self.has_edit_permission(request):
            queryset._for_write = False
            queryset._db = queryset.db
        else:
            queryset._for_write = True
            queryset._db = queryset.db
        return queryset

    def get_model_perms(self, request):

        return {
            'add': self.has_add_perm(request),
            'edit': self.has_edit_perm(request),
            'change': self.has_change_perm(request),
            'delete': self.has_delete_perm(request),
        }

    def has_delete_permission(self, request, obj=None):
        '''add inspection of changeable and editable option
        '''
        if self.editable:
            return super(ProxyModelAdmin, self).has_delete_permission(request, obj)
        return False

    def has_delete_perm(self, request, obj=None):
        '''user permission checking inside the view logic
        '''
        return super(ProxyModelAdmin, self).has_delete_permission(request, obj)

    def has_edit_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('edit', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_edit_perm(self, request, obj=None):
        '''user permission checking inside the view logic
        '''
        return self.has_edit_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        '''add inspection of changeable option
        '''
        return self.has_change_perm(request, obj)
        # ret = False
        # if obj:
        #     if self.editable:
        #         ret = self.has_change_perm(request, obj)
        # else:
        #     ret = self.has_change_perm(request, obj)
        # return ret

    def has_change_perm(self, request, obj=None):
        '''user permission checking inside the view logic
        '''
        return super(ProxyModelAdmin, self).has_change_permission(request, obj)

    def has_add_permission(self, request):
        '''add inspection of addable and editable option
        '''
        if self.addable and self.editable:
            return super(ProxyModelAdmin, self).has_add_permission(request)
        return False

    def has_add_perm(self, request):
        '''user permission checking inside the view logic
        '''
        return super(ProxyModelAdmin, self).has_add_permission(request)

    def get_user_queryset(self, queryset):
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        if 'fields' in kwargs:
            fields = kwargs.get('fields')
        else:
            # 'get_fieldsets' would call 'get_form' again with kwargs: field=None
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))

        # get a blank form to fetch all fields
        form = modelform_factory(self.model, kwargs.get('form', self.form), exclude=())

        if fields is None or fields is forms.ALL_FIELDS:
            fields = form.base_fields.keys()

        readonly_fields = self.get_readonly_fields(request, obj, fields=fields)
        readonly_fields_set = set(readonly_fields)

        if 'exclude' not in kwargs:
            if self.exclude is None:
                exclude = []
            else:
                exclude = list(self.exclude)
            exclude.extend(readonly_fields)

            to_exclude_fields = []
            for name in fields:
                field = form.base_fields.get(name, None)
                if field is None:
                    continue
                val = field.prepare_value(getattr(obj, name, None))
                if val is None:
                    continue
                elif name in readonly_fields_set:
                    continue
                elif isinstance(field, forms.ModelMultipleChoiceField):
                    relates = list(val.all().values_list('pk', flat=True))
                    if not relates:
                        continue
                    queryset = self.get_user_queryset(field.queryset)
                    key = field.to_field_name or 'pk'
                    if len(relates) != queryset.filter(**{'%s__in' % key: relates}).count():
                        to_exclude_fields.append(name)
                        readonly_fields_set.add(name)
                elif isinstance(field, forms.ModelChoiceField):
                    queryset = self.get_user_queryset(field.queryset)
                    key = field.to_field_name or 'pk'
                    if not queryset.filter(**{key: val}).exists():
                        to_exclude_fields.append(name)
                        readonly_fields_set.add(name)
                elif isinstance(field, forms.ChoiceField):
                    if field.choices and val not in dict(field.choices):
                        to_exclude_fields.append(name)
                        readonly_fields_set.add(name)

            if to_exclude_fields:
                exclude.extend(to_exclude_fields)
                readonly_fields.extend(to_exclude_fields)
            kwargs['exclude'] = exclude

        kwargs['fields'] = fields
        form = super(ProxyModelAdmin, self).get_form(request, obj, **kwargs)
        # remove the custom fields from base_fields which is in 'exlcude' or not
        # in 'fields' to prevent from checking these fields
        exclude = form._meta.exclude or ()
        for name in form.declared_fields:
            if name in exclude or name not in fields:
                form.base_fields.pop(name, None)
        return form

    def history_view(self, request, object_id, extra_context=None):
        '''
        The 'history' modeladmin view for this model.

        Combine all real models' history into concrete model history view
        '''
        from django.contrib.admin.models import LogEntry
        # First check if the user can see this history.
        model = self.model
        obj = get_object_or_404(model, pk=unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        # Then get the history for this object.
        opts = model._meta
        app_label = opts.app_label
        content_types = [ContentType.objects.get_for_model(model, for_concrete_model=False)]
        for submodel in model.__subclasses__():
            content_types.append(ContentType.objects.get_for_model(submodel, for_concrete_model=False))
        action_list = LogEntry.objects.filter(
            object_id=unquote(object_id),
            content_type__in=content_types,
        ).select_related().order_by('-action_time')

        context = dict(
            self.admin_site.each_context(request),
            title=_('Change history: %s') % force_text(obj),
            action_list=action_list,
            module_name=capfirst(force_text(opts.verbose_name_plural)),
            object=obj,
            app_label=app_label,
            opts=opts,
            preserved_filters=self.get_preserved_filters(request),
        )
        context.update(extra_context or {})

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.object_history_template or [
            "admin/%s/%s/object_history.html" % (app_label, opts.model_name),
            "admin/%s/object_history.html" % app_label,
            "admin/object_history.html"
        ], context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super(ProxyModelAdmin, self).get_fieldsets(request, obj))
        if not self.has_change_perm(request, obj):
            list_display = self.get_list_display(request)
            valid_f_names = flatten_fieldsets(fieldsets)
            fields = [f for f in list_display if f in valid_f_names]
            return [(None, {'fields': fields})]
        return fieldsets

    def get_readonly_fields(self, request, obj=None, fields=None):
        if obj and self.has_edit_perm(request, obj):

            readonly_fields = list(super(ProxyModelAdmin, self).get_readonly_fields(request, obj))
            readonly_fields_set = set(readonly_fields)
            for field in self.change_view_readonly_fields:
                if field not in readonly_fields_set:
                    readonly_fields_set.add(field)
                    readonly_fields.append(field)

            editable_fields = self.get_editable_fields(request, obj)
            if editable_fields is not None:
                editable_fields_set = set(editable_fields)
                declared_fields = self.fieldsets
                if declared_fields:
                    declared_fields = flatten_fieldsets(declared_fields)
                else:
                    declared_fields = [f.name for f in self.opts.fields]
                for field in declared_fields:
                    if (field not in editable_fields_set
                            and field not in readonly_fields_set):
                        readonly_fields_set.add(field)
                        readonly_fields.append(field)
            return readonly_fields
        elif not self.has_edit_perm(request, obj):
            return fields if fields is not None else self.get_list_display(request)
        else:
            return list(super(ProxyModelAdmin, self).get_readonly_fields(request, obj))

    def get_list_display(self, request):
        '''
        get all fields except PK and Relations if extend_normal_fields is True
        '''

        list_display = list(super(ProxyModelAdmin, self).get_list_display(request))
        if not hasattr(request, '_access_rels'):
            request._access_rels = []

            def _add_access_rels(rel, is_foreign_key):

                target_field, remote_field = get_related_model_fields(self.model, rel, is_foreign_key)
                rel_opts = remote_field.model._meta
                codename = get_permission_codename('change', rel_opts)
                if request.user.has_perm('%s.%s' % (rel_opts.app_label, codename)):
                    try:
                        uri = reverse('admin:%s_%s_changelist' % (
                            rel_opts.app_label, rel_opts.model_name))
                    except NoReverseMatch:
                        pass
                    else:
                        request._access_rels.append((uri, target_field, remote_field, is_foreign_key))

            for rel in self.opts.related_objects:
                #  + tuple(r.remote_field for r in self.opts.many_to_many):
                _add_access_rels(rel, False)
            for key, field in self.opts._forward_fields_map.items():
                if key != field.name:
                    continue
                if field.is_relation and (field.many_to_one or field.one_to_one) \
                        and hasattr(field.remote_field, 'model') and field.remote_field.model:
                    _add_access_rels(field.remote_field, True)

        if request._access_rels:
            self._access_rels = request._access_rels
        else:
            self._access_rels = request._access_rels

        if not self.extend_normal_fields:
            if self._access_rels:
                list_display.append('get_all_relations')
            return list_display

        field_names = []
        heads = []
        middles = []
        tails = []

        def _get_field(field_name):
            if not field_name or not isinstance(field_name, six.string_types):
                return field_name
            try:
                field = self.model._meta.get_field(field_name)
                if field and isinstance(field, models.ImageField):
                    return format_field(field.verbose_name, field.name)
                else:
                    return field_name
            except FieldDoesNotExist:
                return field_name

        while list_display:
            name = list_display.pop(0)
            if name in self.tails:
                tails.append(_get_field(name))
            elif name in self.heads:
                heads.append(_get_field(name))
            else:
                middles.append(_get_field(name))

        for field in self.get_normal_fields():
            if field.name in heads or field.name in middles or field.name in tails:
                continue
            if field.name in self.exclude_list_display:
                pass
            elif field.name in self.tails:
                tails.append(_get_field(field.name))
            elif field.name in self.heads:
                heads.append(_get_field(field.name))
            else:
                middles.append(_get_field(field.name))
        field_names.extend(heads)
        field_names.extend(middles)
        field_names.extend(tails)
        if self._access_rels:
            field_names.append('get_all_relations')
        return field_names

    # def _get_image_field_render(self, field):
    #     def image_tag(obj):
    #         return mark_safe('<img src="%s" style="max-width: 500px; max-height:300px" />'
    #             % (getattr(obj, field.name)))
    #     image_tag.short_description = field.verbose_name
    #     return image_tag

    def get_normal_fields(self):
        fields = []
        exclude = self.exclude or ()
        for field in self.model._meta.concrete_fields:
            if not (isinstance(field, RelatedField)
                    or field.name.startswith('_')
                    or field.attname in exclude):
                if isinstance(field, models.ImageField):
                    # field_name = '_apiview__%s__image_show' % field.name
                    # if not hasattr(self, field_name):
                    #     setattr(self, field_name, self._get_image_field_render(field))
                    # field = field.clone()
                    # field.name = field_name
                    fields.append(field)
                elif not isinstance(field, models.FileField):
                    fields.append(field)
        return fields

    def get_all_relations(self, obj):
        if not self._access_rels:
            return ''
        html_list = ['<select onchange="window.open(this.value, \'_self\');">', ]
        html_list.append('<option value="" selected="selected">------</option>')
        for uri, target_field, remote_field, is_foreign_key in self._access_rels:
            rel_opts = remote_field.model._meta
            value = getattr(obj, target_field.attname)
            value = force_text(value)
            params = {remote_field.name: value}
            url = '%s?%s' % (uri, urlencode(params))
            if is_foreign_key:
                html_list.append('<option value="%s">%s</option>' % (url, target_field.verbose_name))
            else:
                html_list.append('<option value="%s">%s-%s</option>' % (
                    url, rel_opts.verbose_name, remote_field.verbose_name))
        html_list.append('</select>')
        return mark_safe(''.join(html_list))

    get_all_relations.short_description = '相关项'
    get_all_relations.allow_tags = True


def check_perms(*perms):
    """
    Returns True if the given request has permissions to manage an object.
    """

    def inner(func):
        @wraps(func)
        def wrapper(admin, request, *args, **kwargs):
            opts = admin.opts
            for perm in perms:
                codename = get_permission_codename(perm, opts)
                if not request.user.has_perm(
                                "%s.%s" % (opts.app_label, codename)):
                    raise PermissionDenied
            return func(admin, request, *args, **kwargs)

        return wrapper

    return inner


class ImportMixin(_ImportMixin):
    @check_perms('add', 'edit')
    def import_action(self, request, *args, **kwargs):
        return _ImportMixin.import_action(self, request, *args, **kwargs)

    @check_perms('add', 'edit')
    def process_import(self, request, *args, **kwargs):
        return _ImportMixin.process_import(self, request, *args, **kwargs)

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model, resource_class=BaseModelResource)
        elif self.resource_class._meta.model is None:
            return modelresource_factory(self.model, resource_class=self.resource_class)
        else:
            return self.resource_class


class LimitQuerySetMixin(object):
    LIMIT = None

    def count(self):
        count = super(LimitQuerySetMixin, self).count()
        if self.LIMIT > 0:
            return min(count, self.LIMIT)
        return count

    @classmethod
    def from_queryset(cls, other, **kwargs):
        '''根据其他QuerySet对象的数据生成实例'''
        query = other.query.clone()
        if other._sticky_filter:
            query.filter_is_sticky = True
        clone = cls(model=other.model, query=query, using=other._db, hints=other._hints)
        clone._for_write = other._for_write
        clone._prefetch_related_lookups = other._prefetch_related_lookups[:]
        clone._known_related_objects = other._known_related_objects
        clone._iterable_class = other._iterable_class
        clone._fields = other._fields

        clone.__dict__.update(kwargs)
        return clone

    def iterator(self):
        if self.LIMIT is not None:
            if self.query.low_mark >= self.LIMIT:
                return iter(())
            elif (self.query.high_mark is None
                  or self.query.high_mark > self.LIMIT):
                new_qs = self._clone()
                new_qs.query.high_mark = self.LIMIT
                return new_qs.iterator()
        return super(LimitQuerySetMixin, self).iterator()


class DynQuerySet(LimitQuerySetMixin, QuerySet):
    LIMIT = None

    def __getstate__(self):
        '''pickle adapt, to prevent _fetch_all data'''
        obj_dict = self.__dict__.copy()
        obj_dict[DJANGO_VERSION_PICKLE_KEY] = get_version()
        return obj_dict


def mail_export_data(filename, to, model, resource_class, format_class, queryset):
    '''
    Used to export data
    '''
    if not resource_class._meta.model:
        resource = modelresource_factory(model, resource_class=resource_class)()
    else:
        resource = resource_class()
    file_format = format_class()

    data = resource.export(queryset)
    export_data = file_format.export_data(data)

    content_type = mimetypes.guess_type(filename)[0]
    mailtools.mail(
        '导出结果：' + filename,
        to=to,
        body='请查看附件',
        attachments=[(filename, export_data, content_type)])


class HumanizedModelResource(BaseModelResource):
    '''
    Humanize related fields' value

    Note: this would slow down export processing, even if get related objects
          with 'prefetch_related' to access DB once per field

          to be more efficiency, overwrite 'get_export_date' like this:

            def get_export_data(self, file_format, queryset):
                fields = ["related_field1", ]
                headers = ["related_header1", ]
                for field in self.get_normal_fields():
                    fields.append(field.attname)
                    headers.append(field.verbose_name)

                data = tablib.Dataset(headers=headers)
                for row in queryset.values_list(*fields):
                    data.append(row)
                return file_format.export_data(data)

    '''

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        field = super(HumanizedModelResource, cls).field_from_django_field(
            field_name, django_field, readonly
        )
        if field:
            localize_method = 'dehydrate_%s' % field_name
            if django_field.choices:
                setattr(cls, localize_method, lambda self, obj: getattr(obj, 'get_%s_display' % django_field.name)())
            elif isinstance(django_field, RelatedField):
                setattr(cls, localize_method,
                        lambda self, obj: force_text(getattr(obj, django_field.name)))
        return field


class ExportMixin(_ExportMixin):

    def async_export_data(self, func, *args, **kwargs):
        func(*args, **kwargs)

    @check_perms('change')
    def export_action(self, request, *args, **kwargs):
        if request.method == "POST":
            if not request.user.email:
                self.message_user(request, '请设置您的邮箱, 以接收导出数据', messages.ERROR)
            elif not request.POST['file_format']:
                # prompt error
                return _ExportMixin.export_action(self, request, *args, **kwargs)
            else:
                formats = self.get_export_formats()
                try:
                    format_index = int(request.POST['file_format'])
                    file_format = formats[format_index]()
                except Exception:
                    raise Http404

                # from swanleaf.celery.celeryTasks import async_call
                filename = self.get_export_filename(file_format)
                queryset = self.get_export_queryset(request)
                queryset = DynQuerySet.from_queryset(queryset)
                # queryset = queryset.using(BSlave.db_slave1)
                # queryset = queryset.using(DEFAULT_DB_ALIAS)
                if self.resource_class is None:
                    if isinstance(self, ImportMixin):
                        resource_class = BaseModelResource
                    else:
                        resource_class = HumanizedModelResource
                else:
                    resource_class = self.resource_class

                # if (config.SL_EXPORT_DATA_NUM > 0
                #         and queryset.count() > config.SL_EXPORT_DATA_NUM):
                #
                #     if config.SL_EXPORT_DATA_STRICT:
                #         self.message_user(
                #             request,
                #             '导出数据量超出限制(%s条)，请添加筛选条件后重试' % (
                #                 config.SL_EXPORT_DATA_NUM, ),
                #             messages.ERROR)
                #         return HttpResponseRedirect('../?' + request.META['QUERY_STRING'])
                #     else:
                #         self.message_user(
                #             request, '导出数据量过多，处理时间较长，请耐心等待邮件',
                #             messages.WARNING)
                self.async_export_data(mail_export_data, filename, request.user.email, self.model,
                                       resource_class, formats[format_index], queryset)
                # mail_export_data(filename, request.user.email, self.model,
                #                  resource_class, formats[format_index], queryset)
                # async_call(
                #     mail_export_data, filename, request.user.email, self.model,
                #     resource_class, formats[format_index], queryset)

                self.message_user(
                    request, '数据将发送到您的邮箱, 请注意查收',
                    messages.SUCCESS)
            return HttpResponseRedirect('../?' + request.META['QUERY_STRING'])
        return _ExportMixin.export_action(self, request, *args, **kwargs)

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model, resource_class=HumanizedModelResource)
        elif self.resource_class._meta.model is None:
            return modelresource_factory(self.model, resource_class=self.resource_class)
        else:
            return self.resource_class


class ImportExportMixin(ImportMixin, ExportMixin):
    change_list_template = _ImportExportMixin.change_list_template
