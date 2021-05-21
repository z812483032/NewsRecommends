# encoding: utf-8
"""
Definition of the rest framework compatible view class
"""
from __future__ import absolute_import

import six

from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response

from .base import ViewMetaclass, ViewOptions
from .param import Param


class APIViewOptions(ViewOptions):
    """APIView options class

    Extend options:
    * wrappers          view's wrappers generate with the nearest-first logic,
                        this attribute will generate all parents' wrappers
    """

    def __init__(self, options=None, parent=None):
        super(APIViewOptions, self).__init__(options, parent)
        self.wrappers = list(reversed(getattr(options, 'wrappers', ())))

        if self.parent:
            self.wrappers.extend(parent._meta.wrappers)

    def wrap_view(self, view):
        for wrapper in self.wrappers:
            view = wrapper(view)
        return view


class View(six.with_metaclass(ViewMetaclass, APIView)):
    """
    Rest-Framework compatible view
    """

    option_class = APIViewOptions

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.http_method_names = self.http_method_names + ["ws", ]

    def get_renderer_context(self):
        context = super(View, self).get_renderer_context()
        context.update({
            'view_options': self._meta,
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        ___ = request.body  # NOQA
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers
        self.is_ws = kwargs.get("is_ws", False)
        self.ws_data = kwargs.get("ws_data", {})
        self.ws_reply_channel = kwargs.get("ws_reply_channel", None)
        ws_user = kwargs.get("ws_user", None)
        if ws_user is not None:
            request.user = ws_user
        try:
            self.initial(request, *args, **kwargs)
            handler_name = request.method.lower()
            if self.is_ws:
                handler_name = "ws"
            if handler_name in self.http_method_names:
                # opts = self._meta
                if hasattr(self, handler_name):
                    handler = getattr(self, handler_name)
                    if not getattr(handler, '_decorated', False):
                        decorated_handler = self._meta.decorate_handler(handler)
                        if decorated_handler is not handler:
                            decorated_handler.__dict__['_decorated'] = True
                            setattr(self, handler_name, decorated_handler)
                            handler = decorated_handler
                else:
                    handler = self.http_method_not_allowed

                request.params = Param(self, request, kwargs, self.is_ws, self.ws_data)
                request._request.params = request.params
                response = handler(request, *args, **kwargs)
            else:
                handler = self.http_method_not_allowed
                response = handler(request, *args, **kwargs)
        except forms.ValidationError as exc:
            response = self.handle_param_errors(exc)
        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def handle_param_errors(self, exc):
        if hasattr(exc, 'error_dict'):
            return Response(exc.error_dict, status=400)
        else:
            return Response({'*': exc}, status=400)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(View, cls).as_view(*args, **kwargs)
        return cls._meta.wrap_view(view)
