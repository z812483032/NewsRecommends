#! usr/bin/env python
# encoding: utf-8

from datetime import timedelta
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.contenttypes.models import ContentType


class AbstractFieldListFilter(admin.FieldListFilter):
    filter_parameter = None
    url_parameter = None

    def get_parameter_name(self, field_path):
        """ Query parameter name for the URL """
        if self.url_parameter:
            return self.url_parameter
        raise NotImplementedError

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.parameter_name = self.get_parameter_name(field_path)
        super(AbstractFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def has_output(self):
        """ Whether to show filter """
        return True

    def lookups(self, request, model_admin):
        """ Not using lookups """
        return ()

    def choices(self, cl):
        """ Not used, but required by admin_list_filter template tag """
        return ()

    def queryset(self, request, queryset):
        """ Does the actual filtering """
        if self.used_param():
            filter_parameter = self.filter_parameter if self.filter_parameter else self.parameter_name
            return queryset.filter(**{filter_parameter: self.used_param()})

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]

    def used_param(self):
        """ Value from the query string"""
        return self.used_parameters.get(self.parameter_name, '')


class RelatedAutocompleteFilter(AbstractFieldListFilter):
    template = 'apiview/related_autocomplete.html'
    model = None

    def get_parameter_name(self, field_path):
        if self.url_parameter:
            field_path = self.url_parameter
        # use related field itself to prevent 'join' statement in DB
        return u'{0}__exact'.format(field_path)

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(RelatedAutocompleteFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        field_model = field.model or self.model
        if field_model:
            content_type = ContentType.objects.get_for_model(
                getattr(field_model, field.name).field.remote_field.model, for_concrete_model=False
            )
            self.grappelli_trick = u'/{app_label}/{model_name}/{to_field_var}={to_field}'.format(
                to_field_var=TO_FIELD_VAR,
                app_label=content_type.app_label,
                model_name=content_type.model,
                to_field=getattr(field, 'to_fields', ('id', ))[0]
            )


class SearchFilter(AbstractFieldListFilter):
    template = 'apiview/search.html'

    def get_parameter_name(self, field_path):
        return u'{0}__exact'.format(field_path)


class ISearchFilter(SearchFilter):
    """ Case-insensitive serach filter """

    def get_parameter_name(self, field_path):
        return u'{0}__iexact'.format(field_path)


# compat
SearchFilterC = ISearchFilter


class StartswithFilter(SearchFilter):
    def get_parameter_name(self, field_path):
        return u'{0}__startswith'.format(field_path)


class IStartswithFilter(SearchFilter):
    def get_parameter_name(self, field_path):
        return u'{0}__istartswith'.format(field_path)


class ContainsFilter(SearchFilter):
    def get_parameter_name(self, field_path):
        return u'{0}__contains'.format(field_path)


class IContainsFilter(SearchFilter):
    def get_parameter_name(self, field_path):
        return u'{0}__icontains'.format(field_path)


class DateFieldListFilter(admin.FieldListFilter):
    template = 'apiview/date_filter.html'

    lookup_suffix = ['exact', 'gte', 'lte', 'isnull', 'lt']

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(DateFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        self.parameter_name = self.field_path

    def expected_parameters(self):
        return [self.patch_param(suffix)
                for suffix in self.lookup_suffix]

    def queryset(self, request, queryset):
        used_parameters = self.used_parameters
        if isinstance(self.field, models.DateTimeField):
            compat_parameters = self.compat_datetimefield()
        else:
            compat_parameters = self.used_parameters
        self.used_parameters = compat_parameters
        queryset = super(DateFieldListFilter, self).queryset(request, queryset)
        self.used_parameters = used_parameters
        return queryset

    def compat_datetimefield(self):
        compat_parameters = {}
        for k, v in self.used_parameters.items():
            if k.endswith('exact'):
                v = self.field.to_python(v)
                compat_parameters[self.patch_param('gte')] = v
                compat_parameters[self.patch_param('lt')] = v + timedelta(days=1)
            elif k.endswith('lte'):
                v = self.field.to_python(v)
                compat_parameters[self.patch_param('lt')] = v + timedelta(days=1)
            else:
                compat_parameters[k] = v
        return compat_parameters

    def patch_param(self, suffix):
        return '%s__%s' % (self.field_path, suffix)

    def __getattribute__(self, attr):
        '''
        extend attributes 'val_%' to get specified parameter
        '''
        if attr.startswith('val_'):
            suffix = attr[4:]
            if suffix in self.lookup_suffix:
                return self.used_parameters.get(self.patch_param(suffix)) or ''
            else:
                raise AttributeError('%s has no attribute "%s"' % (self, attr))
        return super(DateFieldListFilter, self).__getattribute__(attr)

    def choices(self, cl):
        return ()


class RangeFilter(admin.FieldListFilter):
    template = 'apiview/range_filter.html'

    lookup_suffix = ['gte', 'lte', ]

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(RangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        self.parameter_name = self.field_path

    def expected_parameters(self):
        return [self.patch_param(suffix) for suffix in self.lookup_suffix]

    def patch_param(self, suffix):
        return '%s__%s' % (self.field_path, suffix)

    def __getattribute__(self, attr):
        '''
        extend attributes 'val_%' to get specified parameter
        '''
        if attr.startswith('val_'):
            suffix = attr[4:]
            if suffix in self.lookup_suffix:
                return self.used_parameters.get(self.patch_param(suffix)) or ''
            else:
                raise AttributeError('%s has no attribute "%s"' % (self, attr))
        return super(RangeFilter, self).__getattribute__(attr)

    def choices(self, cl):
        return ()
