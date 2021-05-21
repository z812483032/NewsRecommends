# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import six

from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from . import utility


class DictChoiceField(serializers.ChoiceField):

    def __init__(self, choices, **kwargs):
        super(DictChoiceField, self).__init__(choices, **kwargs)
        self.choice_strings_to_values = {
            six.text_type(key): {'key': key, 'desc': self.choices[key]} for key in self.choices.keys()
            }


class DateStampField(serializers.DateField):
    def to_representation(self, value):
        return utility.datetime2timestamp(value)

    def to_internal_value(self, data):
        return utility.timestamp2datetime(int(data)).date()


class DateTimeStampField(serializers.DateTimeField):
    def to_representation(self, value):
        return utility.datetime2timestamp(value)

    def to_internal_value(self, data):
        return utility.timestamp2datetime(int(data))


# class DateFormatField(serializers.DateField):
#     def __init__(self, format=empty, input_formats=None, *args, **kwargs):
#         if format == empty:
#             format = settings.DATE_FORMAT
#         super(DateFormatField, self).__init__(format=format, input_formats=input_formats, *args, **kwargs)
#
#
# class DateTimeFormatField(serializers.DateTimeField):
#     def __init__(self, format=empty, input_formats=None, *args, **kwargs):
#         if format == empty:
#             format = settings.DATETIME_FORMAT
#         super(DateTimeFormatField, self).__init__(format=format, input_formats=input_formats, *args, **kwargs)
#
#
# class TimeFormatField(serializers.TimeField):
#     def __init__(self, format=empty, input_formats=None, *args, **kwargs):
#         if format == empty:
#             format = settings.TIME_FORMAT
#         super(TimeFormatField, self).__init__(format=format, input_formats=input_formats, *args, **kwargs)

#
# class FileField(serializers.FileField):
#     def to_representation(self, value):
#         import pdb;pdb.set_trace()
#         return super(FileField, self).to_representation(value)
#     # def to_internal_value(self, value):
#     #     pass
#
#
# class ImageField(serializers.ImageField):
#     def to_representation(self, value):
#         return super(ImageField, self).to_representation(value)
#     # def to_internal_value(self, value):
#     #     pass
#
#
# class FilePathField(serializers.FilePathField):
#     def to_representation(self, value):
#         pass
#     def to_internal_value(self, value):
#         pass

# class SerializerMetaclass(serializers.SerializerMetaclass):
#     '''处理兼容问题'''
#     def __new__(cls, name, bases, attrs):
#         new_attrs = {}
#         import pdb; pdb.set_trace()
#         for att, val in attrs.items():
#             # 与默认方法名冲突的兼容性问题，
#             # 按照新的Field声明规则，重新声明，保持除method_name外其他参数一致
#             if (isinstance(val, serializers.SerializerMethodField)
#                     and val.method_name == b'get_' + att):
#                 if val._args:
#                     args = val._args[1:]
#                     kwargs = val._kwargs
#                 else:
#                     args = val._args
#                     kwargs = val._kwargs
#                     kwargs.pop('method_name', None)
#                 val = serializers.SerializerMethodField(*args, **kwargs)
#             new_attrs[att] = val
#         return super(SerializerMetaclass, cls).__new__(cls, name, bases, new_attrs)
#

# @six.add_metaclass(SerializerMetaclass)
class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        if data is None:
            data = empty

        request = kwargs.pop("request", None)
        context = kwargs.get("context", {})
        if request is not None:
            context.update({"request": request})

        super(BaseSerializer, self).__init__(instance, data, **kwargs)
        self._context = context
        root = self.root
        if root is not None:
            root._context = context
        fields = self._readable_fields
        for field in fields:
            if isinstance(field, BaseSerializer):
                if not hasattr(field, '_context'):
                    field._context = context

        # self.serializer_field_mapping[models.DateField] = DateFormatField
        # self.serializer_field_mapping[models.DateTimeField] = DateTimeFormatField
        # self.serializer_field_mapping[models.TimeField] = TimeFormatField
        # self.serializer_field_mapping[models.FileField] = FileField
        # self.serializer_field_mapping[models.ImageField] = ImageField
        self.serializer_choice_field = DictChoiceField

    def __new__(cls, *args, **kwargs):
        # We override this method in order to automagically create
        # `ListSerializer` classes instead when `many=True` is set.
        request = kwargs.pop("request", None)
        if "context" not in kwargs and request is not None:
            kwargs["context"] = {"request": request}
        return super(BaseSerializer, cls).__new__(cls, *args, **kwargs)

    @property
    def request(self):
        return self.context.get("request", None)

    def to_representation(self, instance):
        return super(BaseSerializer, self).to_representation(instance)

    @property
    def data(self):
        # 新版data属性使用需要一些前置条件，因此重载使之可以直接使用
        if self.instance is None:
            if hasattr(self, 'many'):
                return []
            else:
                return None
        elif hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            self.is_valid()
        return super(BaseSerializer, self).data

    def build_standard_field(self, field_name, model_field):

        return super(BaseSerializer, self).build_standard_field(field_name, model_field)


class DateStampSerializer(BaseSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super(DateStampSerializer, self).__init__(instance, data, **kwargs)
        self.serializer_field_mapping[models.DateField] = DateStampField


class DateTimeStampSerializer(BaseSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super(DateTimeStampSerializer, self).__init__(instance, data, **kwargs)
        self.serializer_field_mapping[models.DateTimeField] = DateTimeStampField

# class DynamicFieldsModelSerializer(BaseSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
#
#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
#
#         if fields:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
