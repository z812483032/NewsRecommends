#! usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from django.apps import AppConfig


class ApiViewConfig(AppConfig):
    name = 'apiview'

    def ready(self):
        # 后台filter自定义
        from django.contrib import admin
        from django.db import models
        from apiview.filters import (
            RelatedAutocompleteFilter, DateFieldListFilter,
        )

        def _autocomplete_filter_check(field):
            '''
            check field to use RelatedAutocompleteFilter
            '''
            if field.remote_field:
                return getattr(field.remote_field.model, 'AJAX_FILTER', True)
            elif isinstance(field, models.ForeignKey):
                return True
            return False

        admin.FieldListFilter.register(
            _autocomplete_filter_check,
            RelatedAutocompleteFilter,
            take_priority=True
        )

        admin.FieldListFilter.register(
            lambda field: isinstance(field, models.DateField),
            DateFieldListFilter,
            take_priority=True
        )

        # 防止关联查询
        class _RelatedFieldListFilter(admin.RelatedFieldListFilter):
            def __init__(self, field, request, params, model, model_admin, field_path):
                super(_RelatedFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
                self.lookup_kwarg = '%s__exact' % field_path
                self.lookup_val = request.GET.get(self.lookup_kwarg)

        admin.FieldListFilter.register(
            lambda f: f.remote_field,
            _RelatedFieldListFilter,
            take_priority=True
        )
