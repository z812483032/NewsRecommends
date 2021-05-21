# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import json
import six
from hashlib import md5

from io import BytesIO
from StringIO import StringIO
from importlib import import_module

from django.conf import settings
from django import http, forms
from django.db import models, transaction
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _
from django.utils import datastructures
from django.utils.functional import SimpleLazyObject, cached_property

TEST_PARAM = '_test_case_'
# md5('testing-gg-5566').hexdigest()
TEST_KEY = '8F7CE16E134926D721AB3D109714DF42'
TEST_REQUEST_PARAM = '_test_case_request_'


class JSONFormField(forms.CharField):

    def to_python(self, value):
        if value in self.empty_values:
            return None
        return json.loads(value)

    def prepare_value(self, value):
        value = self.to_python(value)
        if value is not None:
            value = json.dumps(value, indent=4)
        return value


class JSONField(models.TextField):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            return json.loads(value)
        return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        val = self.to_python(val)
        return json.dumps(val)

    def get_prep_value(self, value):
        if not value:
            return ''
        return json.dumps(self.to_python(value))

    def formfield(self, **kwargs):
        defaults = {'form_class': JSONFormField}
        defaults.update(**kwargs)
        return super(JSONField, self).formfield(**defaults)


class TestCase(models.Model):
    path = models.CharField(_('path'), max_length=100, db_index=True)
    request_md5 = models.CharField(_('md5'), max_length=32, db_index=True, editable=False)
    request_data = JSONField(_('request data'))
    response_data = JSONField(_('response data'), blank=True)
    response_schema = JSONField(_('response schema'), blank=True)

    def __unicode__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.request_md5)

    def as_request(self):
        assert self.request_data, 'Could not construct an empty TestCase object'
        request = http.HttpRequest()
        data = self.request_data_dict
        request.path = data['path']
        request.method = data['method']
        request.path_info = data['path_info']
        request._body = data['body']
        request.META = data['headers']
        request._encoding = data['encoding']
        request._stream = StringIO()
        request._read_started = False
        request._post_parse_error = False
        request.resolver_match = None

        request._load_post_and_files()
        query_string = '%s&%s=1' % (data['query_string'], TEST_REQUEST_PARAM)
        request.GET = http.QueryDict(query_string, encoding=request.encoding)
        request.POST = getattr(request, '_post')
        request.FILES = getattr(request, '_files')
        request.COOKIES = http.parse_cookie(request.META.get('HTTP_COOKIE', b''))
        request.REQUEST = datastructures.MergeDict(request.POST, request.GET)

        # extra attributes added by middlewares
        from django.contrib.auth.middleware import get_user
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore(request.COOKIES.get(settings.SESSION_COOKIE_NAME, None))
        request.user = SimpleLazyObject(lambda: get_user(request))
        return request

    def as_response(self):
        assert self.response_data, 'Could not construct an empty TestCase object'
        response = http.HttpResponse()
        data = self.response_data_dict
        response._charset = data['encoding']
        response.status_code = data['status_code']
        response._headers = data['headers']

        response.content = data['content']
        return response

    @property
    def request_data_dict(self):
        if not self.request_data:
            return None
        elif isinstance(self.request_data, six.string_types):
            self.request_data = json.loads(self.request_data)
        return self.request_data

    @property
    def response_data_dict(self):
        if not self.response_data:
            return None
        elif isinstance(self.response_data, six.string_types):
            self.response_data = json.loads(self.response_data)
        return self.response_data

    @property
    def response_schema_dict(self):
        if not self.response_schema:
            return None
        elif isinstance(self.response_schema, six.string_types):
            self.response_schema = json.loads(self.response_schema)
        return self.response_schema

    def load_request(self, request):
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')
        try:
            body = request.body
        except Exception:
            body = request._body = request.read()
            request._stream = BytesIO(request._body)

        request_headers = {}
        for name, value in request.META.items():
            if name.startswith('HTTP_'):
                request_headers[name] = value
            elif name in ('CONTENT_TYPE', ):
                request_headers[name] = value

        request_data = {
            'path': path,
            'encoding': request.encoding or settings.DEFAULT_CHARSET,
            'path_info': request.path_info,
            'method': request.method,
            'query_string': query_string,
            'body': body,
            'headers': request_headers,
        }

        self.path = path
        self.request_data = request_data
        self.request_md5 = md5(json.dumps(self.request_data)).hexdigest()
        try:
            case = TestCase.objects.get(
                    path=self.path,
                    request_md5=self.request_md5)
            self.__dict__ = case.__dict__
        except TestCase.DoesNotExist:
            pass

    def load_response(self, response, confirm=False):
        if self.response_schema and not confirm:
            return

        if hasattr(response, 'render') and callable(response.render):
            response.render()

        content_type = response['Content-Type']
        if 'json' in content_type:
            data_type = 'json'
        elif 'html' in content_type:
            data_type = 'html'
        elif 'xml' in content_type:
            data_type = 'xml'
        else:
            data_type = 'binary'

        response_data = {
            'status_code': response.status_code,
            'type': data_type,
            'encoding': response._charset,
            'headers': response._headers,
            'content': response.content,
            }

        self.response_data = response_data

        schema_method = getattr(self, 'schema_' + data_type, None)
        if schema_method:
            schema = schema_method(response.content)
            self.response_schema = schema
        else:
            schema = None

    def test(self):
        assert self.request_data, 'Could not construct an empty TestCase object'

        match = resolve(self.path)
        with transaction.commit_manually():
            try:
                response = match.func(self.as_request(), *match.args, **match.kwargs)
                return response
            finally:
                transaction.rollback()

    @cached_property
    def test_response(self):
        return self.test()

    @cached_property
    def errors(self):
        return list(self.gen_errors())

    def reset_errors(self):
        self.errors = list(self.gen_errors())

    def validate(self):
        return not bool(next(self.gen_errors(), False))

    def gen_errors(self):
        if not self.response_schema or not self.response_data:
            return

        response = self.test_response
        if hasattr(response, 'render') and callable(response.render):
            response.render()

        data = self.response_data_dict
        validate_method = getattr(self, 'validate_' + data['type'])
        for err in validate_method(response.content):
            yield err

    def schema_json(self, content):
        from .dtd.jsonschema import json2schema, gen_errors, flex_schema_by_errs
        data = json.loads(content)
        if self.response_schema:
            schema = self.response_schema_dict
            errors = list(gen_errors(data, schema))
            flex_schema_by_errs(schema, errors)
        else:
            schema = json2schema(data)
        return schema

    def validate_json(self, content):
        from .dtd.jsonschema import gen_errors
        for err in gen_errors(json.loads(content), json.loads(self.response_schema)):
            yield err
