# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from functools import wraps

from django.db import transaction

from .models import TestCase, TEST_REQUEST_PARAM, TEST_PARAM, TEST_KEY


def testcase(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if (not request.REQUEST.get(TEST_PARAM, '').upper() == TEST_KEY):
            return view(request, *args, **kwargs)
        elif request.REQUEST.get(TEST_REQUEST_PARAM, '') == '1':
            with transaction.commit_manually():
                try:
                    return view(request, *args, **kwargs)
                finally:
                    transaction.rollback()

        case = TestCase()
        case.load_request(request)

        with transaction.commit_manually():
            try:
                response = view(request, *args, **kwargs)
            finally:
                transaction.rollback()

        case.load_response(response, False)
        case.save()
        return response

    return wrapper
