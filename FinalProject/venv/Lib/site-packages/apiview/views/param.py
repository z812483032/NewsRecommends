# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django import forms
from django.forms.utils import ErrorDict
from django.utils.encoding import force_text
from rest_framework import exceptions


class TextErrorDict(ErrorDict):
    def __str__(self):
        return self.as_text()

    def __unicode__(self):
        return force_text(self.as_text())


class Param(object):
    """
    Wrap django-form to access parameters more conveniently
    """
    def __init__(self, view, request, kwargs=None, is_ws=False, ws_data=None):
        """
        May raise ValidationError when checking is False when accessing parameters
        """
        self._opts = view._meta
        self._request = request
        if is_ws:
            self._bounded_form = view.param_form(ws_data)
        else:
            data = request.REQUEST.copy()
            if kwargs:
                data.update(kwargs)
            args = [data, ]
            try:
                args.append(request.FILES)
            except exceptions.UnsupportedMediaType:
                pass
            self._bounded_form = view.param_form(*args)
        self._dependency = self._opts.param_dependency
        if self._opts.param_managed:
            errors = self._bounded_form.errors
            if errors:
                exc = forms.ValidationError(errors)
                exc.error_dict_obj = errors
                raise exc

            self._cleaned_data = self._bounded_form.cleaned_data

            self._clean_dependency()
        else:
            self._cleaned_data = {}

    @property
    def form(self):
        return self._bounded_form

    @form.setter
    def form(self, other):
        self._bounded_form = other
        if getattr(other, 'cleaned_data', None):
            self._cleaned_data = other.cleaned_data
            self._clean_dependency()
        else:
            self._cleaned_data = {}

    def _clean_dependency(self, name=None):
        if name is None:
            names = self._cleaned_data.keys()
        else:
            names = [name]

        errors = ErrorDict()
        for name in names:
            if name in self._dependency:
                try:
                    field, pairs = self._dependency[name]
                    try:
                        _ = field.clean(self._cleaned_data[name])
                    except forms.ValidationError:
                        continue
                    for sub_name, sub_field in pairs:
                        _ = sub_field.clean(self._cleaned_data[sub_name])  # NOQA
                except forms.ValidationError as exc:
                    error_dict = TextErrorDict([(sub_name, exc.messages)])
                    errors[name] = [error_dict]
                    del self._cleaned_data[name]

        if errors:
            raise forms.ValidationError(errors)

    def __getattr__(self, name):
        if name not in self._cleaned_data:
            form = self._bounded_form
            if name not in form.fields:
                raise AttributeError(name)
            field = form.fields[name]
            value = field.widget.value_from_datadict(
                form.data, form.files, form.add_prefix(name))
            if isinstance(field, forms.FileField):
                initial = self.initial.get(name, field.initial)
                value = field.clean(value, initial)
            else:
                value = field.clean(value)
            self._cleaned_data[name] = value
            self._clean_dependency(name)

        return self._cleaned_data[name]

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self._cleaned_data[name] = value

    def __str__(self):
        return str(self._cleaned_data)
