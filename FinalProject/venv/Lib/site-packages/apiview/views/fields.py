# encoding: utf-8

"""
Wrap django form fields to use `omit`, `default` instead of `required`

重载Django fields以获取对omit、default等特性的支持

注意：
    继承时，如果对__init__, to_python, clean 方法进行重写时，如果不调用父级
    方法，则必须使用wrap_field(method=(<上述重写的方法名>...))对子类进行处理，
    参看BooleanField的处理
"""

from __future__ import unicode_literals, absolute_import

import six

from functools import wraps, partial
from django.db import models
from django.forms import fields
from django.forms.models import fields_for_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from apiview import utility
# to prevent Importation-Examination
from django.forms.fields import *  # NOQA

from apiview import validators
from .widgets import BooleanInput, NullBooleanSelect


class _Empty(object):
    def __nonzero__(self):
        return False

    def __str__(self):
        return '<empty>'


empty = _Empty()


def formfield(field, **kwargs):
    kwargs.setdefault('validators', field.validators)
    if isinstance(field, (
            models.AutoField,
            models.PositiveIntegerField,
            models.PositiveSmallIntegerField)):
        return fields.IntegerField(min_value=0, **kwargs)
    else:
        return globals().get(field.get_internal_type(), fields.CharField)(**kwargs)


def field_for_model(model, field, widget=None, localize=None, help_text=None, error_messages=None):
    return fields_for_model(model, [field], None, widget and {field: widget}, formfield,
                            localize is not None and {field: localize} or localize, None,
                            help_text and {field: help_text},
                            error_messages and {field: error_messages})[field]


def field_info(field):

    if isinstance(field, (fields.BooleanField, fields.NullBooleanField)):
        return '0, false; 1, true'

    if hasattr(field, 'choices'):
        return '; '.join([': '.join(map(force_text, choice)) for choice in field.choices])
    help_text_li = []
    for att in ['max_value', 'min_value', 'max_length', 'min_length', 'max_digits', 'sep', 'seps', 'regex']:
        val = getattr(field, att, None)
        if val is not None:
            help_text_li.append('%s: %s' % (att, val))
    if hasattr(field, 'fields'):
        h_text = []
        for f in field.fields:
            if isinstance(f, fields.Field):
                h_text.append("%s" % f.__class__.__name__)
            elif type(f) == type:
                h_text.append("%s" % f.__name__)
            else:
                h_text.append('%s' % f)
        help_text_li.append("fields : (%s)" % ",".join(h_text))
    if hasattr(field, 'field'):
        if isinstance(field.field, fields.Field):
            help_text_li.append("field : %s" % field.field.__class__.__name__)
        elif type(field.field) == type:
            help_text_li.append('field : %s' % field.field.__name__)
        else:
            help_text_li.append('field : %s' % field.field)
    return '; '.join(help_text_li)


def _wrap_field(fieldclass, methods=()):
    '''rewrite the __init__, to_python and clean methods to add more features'''
    init_method = fieldclass.__init__

    @wraps(init_method)
    def __init__(self, *args, **kwargs):
        self.type_name = kwargs.pop('type_name', type(self).__name__)
        if self.type_name.endswith("Field"):
            self.type_name = self.type_name[:-5]
        self.omit = kwargs.pop('omit', empty)
        self.default = kwargs.pop('default', empty)
        if self.omit is not empty:
            kwargs['required'] = False
        elif self.default is not empty:
            kwargs.setdefault('required', True)
        init_method(self, *args, **kwargs)
        self.field_info = field_info(self)

    to_python_method = fieldclass.to_python

    @wraps(to_python_method)
    def to_python(self, value):
        if (value in self.empty_values
                and self.omit is not empty):
            if callable(self.omit):
                return self.omit()
            return self.omit

        value = to_python_method(self, value)

        return value

    clean_method = fieldclass.clean

    @wraps(clean_method)
    def clean(self, *args, **kwargs):
        try:
            return clean_method(self, *args, **kwargs)
        except ValidationError:
            if self.default is not empty:
                if callable(self.default):
                    return self.default()
                return self.default
            raise

    attrs = {
        '__init__': __init__,
        'to_python': to_python,
        'clean': clean,
    }
    if methods:
        all_methods = set(attrs.keys())
        methods = set(methods)
        if methods - all_methods:
            raise TypeError('Unexpected method to be reload: %s' % list(methods - all_methods))
        for item in all_methods - methods:
            attrs.pop(item)

    return type(fieldclass)(fieldclass.__name__, (fieldclass, ), attrs)


def wrap_field(methods=()):
    '''make _wrap_field as a decorator'''
    return partial(_wrap_field, methods=methods)


for _fieldclass_name in fields.__all__[1:]:
    six.exec_('{0} = _wrap_field(fields.{0})'.format(_fieldclass_name))


# overwrite BooleanField and NullBooleanField to accept 0,1
@wrap_field(methods=('to_python', ))
class BooleanField(BooleanField):  # NOQA
    widget = BooleanInput

    default_error_messages = {
        'invalid': _('Enter a valid value.'),
    }

    def to_python(self, value):
        if isinstance(value, six.string_types):
            value = value.lower()
            if value in ('false', '0'):
                value = False
            elif value in ('true', '1'):
                value = True
        return value

    def validate(self, value):
        if value in self.empty_values:
            raise ValidationError(self.error_messages['required'], code='required')
        if not isinstance(value, bool):
            raise ValidationError(self.error_messages['invalid'], code='invalid')


class NullBooleanField(NullBooleanField):  # NOQA
    widget = NullBooleanSelect


class MobileField(CharField):  # NOQA
    default_validators = [validators.mobile]


class LongitudeField(FloatField):  # NOQA
    def __init__(self, max_value=180.0, min_value=-180.0, *args, **kwargs):
        super(LongitudeField, self).__init__(
            max_value=max_value, min_value=min_value, *args, **kwargs
        )


class LatitudeField(FloatField):  # NOQA
    def __init__(self, max_value=90.0, min_value=-90.0, *args, **kwargs):
        super(LatitudeField, self).__init__(
            max_value=max_value, min_value=min_value, *args, **kwargs
        )


class SplitCharField(CharField):  # NOQA
    """Split string value with given sep or seps
    """

    default_field = fields.CharField()

    def __init__(self, *args, **kwargs):
        self.sep = kwargs.pop('sep', ',')
        self.field = kwargs.pop('field', self.default_field)
        super(SplitCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(SplitCharField, self).clean(value)
        if value:
            return list(map(self.field.clean, value.split(self.sep)))
        else:
            return []


class TimestampField(IntegerField):  # NOQA
    def to_python(self, value):
        v = super(TimestampField, self).to_python(value)
        if v is None:
            return None
        return utility.timestamp2datetime(v)


class PairCharField(CharField):  # NOQA
    """Split string value with given seps"""
    default_error_messages = {
        'invalid': _('Enter a valid value.'),
        'unpaired': _('Enter a valid value.'),
    }

    default_field = (fields.CharField(), fields.CharField())

    def __init__(self, *args, **kwargs):
        self.seps = kwargs.pop('seps', ('|', '.'))
        self.fields = kwargs.pop('fields', self.default_field)
        super(PairCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(PairCharField, self).clean(value)
        if value:
            value_list = []
            for val0, val1 in self.gen_split(value):
                value_list.append(
                    (self.fields[0].clean(val0), self.fields[1].clean(val1))
                )
            return value_list
        else:
            return []

    def gen_split(self, value, idx=0):
        if not value:
            return
        if idx == len(self.seps) - 1:
            pair = value.split(self.seps[idx])
            if len(pair) != 2:
                raise ValidationError(
                        self.error_messages['unpaired'],
                        code='unpaired',
                        params={'seps': self.seps},
                    )
            yield value.split(self.seps[idx])
        else:
            for item in value.split(self.seps[idx]):
                for ret in self.gen_split(item, idx + 1):
                    yield ret
