# encoding: utf-8
"""
Declare the metaclass of the views to manage view generation
"""
from __future__ import absolute_import, unicode_literals

import six

from collections import OrderedDict
from six.moves.urllib.parse import urljoin
from django import http
from django import forms
from django.views.generic import View as DjangoView
from django.utils.functional import cached_property
from django.utils.encoding import force_text, force_str

from .utils import split_camel_name
from .param import Param


def _camel2path(name):
    """GenerateURLs => generate/urls"""
    return '/'.join(split_camel_name(name)).lower() + '/'


def _size_len(text):
    return (len(text) + len(text.encode('utf8'))) // 2


def _format(text, size):
    return text + (" " * (size - _size_len(text)))


class ViewOptions(object):
    """View options class

    * name              resolver name of the URL patterns, default is view name
    * path              URL related path generation from parents
    * param_managed     whether manage parameters before dispatching to handler
    * param_fields      parameter's name and field pairs definition,
                        this attribute will generate all parents' param_fields
    * param_dependency  dependency between parameters,
                        format as (name, ((field, [(name, field), ...]), ...))
    * form              form class used to manage parameters
    * decorators        view's decorators generate with the nearest-first logic,
                        this attribute will generate all parents' decorators
    """

    def __init__(self, options=None, parent=None):
        self.view = None
        self.children = []

        self.name = getattr(options, 'name', '')
        self.decorators = list(reversed(getattr(options, 'decorators', ())))

        if parent:
            p_opts = parent._meta
            self.parent = parent
            self.path = getattr(options, 'path', None)
            self.form = getattr(options, 'form', p_opts.form)
            self.param_managed = getattr(options, 'param_managed', p_opts.param_managed)
            self.param_fields = p_opts.param_fields.copy()
            self.param_dependency = p_opts.param_dependency.copy()
            self.param_fields.update(getattr(options, 'param_fields', ()))
            self.param_dependency.update(getattr(options, 'param_dependency', ()))
            self.decorators.extend(p_opts.decorators)
        else:
            self.path = getattr(options, 'path', '/')
            self.parent = None
            self.form = getattr(options, 'form', forms.Form)
            self.param_fields = OrderedDict(getattr(options, 'param_fields', ()))
            self.param_dependency = OrderedDict(getattr(options, 'param_dependency', ()))
            self.param_managed = getattr(options, 'param_managed', True)

    def contribute_to_class(self, cls, name):
        self.view = cls

        if not self.name:
            self.name = self.view.__name__
        if self.path is None:
            parentpath = self.parent._meta.path
            if not parentpath.endswith("/"):
                parentpath += "/"
            self.path = urljoin(parentpath, _camel2path(self.name))
        if self.parent:
            self.parent._meta.children.append(cls)

        form_attrs = dict(self.param_fields)
        form_attrs['__module__'] = cls.__module__
        cls.param_form = type(self.form)(
            force_str(cls.__name__ + 'Form'),
            (self.form, ),
            form_attrs)

        # if cls.__doc__ is None:
        #     cls.__doc__ = ''
        # cls.__doc__ += '\nParameters:\n'
        # cls.__doc__ += self.format_document(with_header=True)

        setattr(cls, name, self)

    @cached_property
    def param_document(self):
        return self.format_document()

    def format_document(self, fields=None, with_header=True):
        if not self.param_fields:
            return ''

        if fields:
            f_attrs = fields
        else:
            f_attrs = ['type_name', 'required', 'omit', 'default', 'help_text', 'field_info']
        fields = ['name'] + f_attrs
        f_lens = [_size_len(field) for field in fields]
        rows = []
        if with_header:
            rows.append(fields)
        for name, field in self.param_fields.items():
            if field.required:
                field_name = '*%s*' % name
            else:
                field_name = '[%s]' % name
            row = [field_name]
            if f_lens[0] < _size_len(field_name):
                f_lens[0] = _size_len(field_name)
            idx = 1
            for att in f_attrs:
                f_val = force_text(getattr(field, att))
                if f_lens[idx] < _size_len(f_val):
                    f_lens[idx] = _size_len(f_val)
                row.append(f_val)
                idx += 1
            rows.append(row)

        doc_list = []
        final_idx = len(rows[0]) - 1
        for row in rows:
            row_doc = []
            for idx, val in enumerate(row):
                if idx == final_idx:
                    row_doc.append(val)
                else:
                    row_doc.append(_format(val, f_lens[idx]))
            doc_list.append(' | '.join(row_doc))

        return '\n'.join(doc_list)

    def decorate_handler(self, handler):
        for decorator in self.decorators:
            handler = decorator(handler)
        return handler


class ViewMetaclass(type):
    """Metaclass of the view classes"""

    def __new__(mcs, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, ViewMetaclass)]
        assert len(parents) <= 1

        __name__ = attrs.pop('__name__', name)

        new_cls = super(ViewMetaclass, mcs).__new__(mcs, name, bases, attrs)

        option_class = getattr(new_cls, 'option_class', ViewOptions)

        if parents:
            opts = option_class(attrs.pop('Meta', None), parents[0])
        else:
            opts = option_class(attrs.pop('Meta', None))

        opts.contribute_to_class(new_cls, '_meta')

        new_cls.__name__ = __name__

        return new_cls


class View(six.with_metaclass(ViewMetaclass, DjangoView)):
    """Base view generated from django view"""

    option_class = ViewOptions

    def dispatch(self, request, *args, **kwargs):
        handler_name = request.method.lower()
        try:
            if handler_name in self.http_method_names:
                # opts = self._meta
                if hasattr(self, handler_name):
                    handler = getattr(self, handler_name)
                else:
                    handler = self.http_method_not_allowed

                request.params = Param(self, request, kwargs)
                response = handler(request, *args, **kwargs)
            else:
                handler = self.http_method_not_allowed
                response = handler(request, *args, **kwargs)

            return response
        except forms.ValidationError as exc:
            response = self.handle_param_errors(exc)

    def handle_param_errors(self, exc):
        if hasattr(exc, 'error_dict'):
            return http.HttpResponseBadRequest(exc.error_dict.as_text())
        else:
            return http.HttpResponseBadRequest(exc)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(View, cls).as_view(*args, **kwargs)
        return cls._meta.decorate_handler(view)
