# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.admin import ModelAdmin, site
from django.utils.translation import ugettext_lazy as _, ungettext
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from .models import TestCase


class TestCaseAdmin(ModelAdmin):
    search_fields = ['path', ]
    list_display = ('request_md5', 'path', 'valid', 'errors')

    readonly = ('path', 'request_md5', 'response_data')

    ordering = ('path', 'id')

    actions = ['delete_selected', 'mark_valid']

    list_per_page = 30

    def mark_valid(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.load_response(obj.test_response, confirm=True)
            obj.save()
            self.log_change(request, obj, 'mark valid')
            count += 1

        self.message_user(request, ungettext(
                'updated %(count)d item',
                'updated %(count)d items',
                count) % {
                    'count': count
            }, messages.SUCCESS)

    mark_valid.short_description = _('mark valid')

    def valid(self, obj):
        try:
            return not obj.errors
        except Exception:
            return False
        return True

    valid.short_description = _('valid')
    valid.boolean = True

    def errors(self, obj):
        error_list = []
        try:
            for err in obj.errors:
                error_list.append('%s: %s' % (' - '.join(map(force_text, err.path)), err.message))
        except Exception as exc:
            error_list.append(force_text(exc))
        return mark_safe('<br/>'.join(error_list))

    errors.short_description = _('errors')


site.register(TestCase, TestCaseAdmin)
