# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.template import Library


register = Library()


@register.inclusion_tag("apiview/scripts.html", takes_context=True)
def apiview(context):
    return context
