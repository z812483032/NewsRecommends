# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.forms import widgets
from django.utils.translation import ugettext_lazy


class BooleanInput(widgets.CheckboxInput):
    def value_from_datadict(self, data, files, name):
        return data.get(name, '')


class NullBooleanSelect(widgets.Select):
    def __init__(self, attrs=None):
        choices = (
            ('0', ugettext_lazy('Unknown')),
            ('1', ugettext_lazy('yes')),
            ('2', ugettext_lazy('no')),
        )
        super(NullBooleanSelect, self).__init__(attrs, choices)
