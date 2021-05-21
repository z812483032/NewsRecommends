# encoding: utf-8
'''
HTML Widget classes for display
'''
from __future__ import absolute_import, unicode_literals

import six
from django import forms
from django.forms.utils import flatatt

from django.utils.html import format_html


def styles2python(str_style):
    dt = {}
    for css_item in str_style.strip().split(';'):
        css_item = css_item.strip()
        if not css_item:
            continue
        attr, val = css_item.split(':')
        dt[attr.strip()] = val.strip()
    return dt


def python2styles(dt_style):
    return '; '.join([': '.join(css_pair) for css_pair in six.iteritems(dt_style)])


class TagWidget(forms.Widget):
    tag = 'span'

    css = None

    def __init__(self, *args, **kwargs):
        super(TagWidget, self).__init__(*args, **kwargs)
        self.attrs['css'] = self._patch_inline_style(self.attrs) or {}
        if self.css:
            for att, val in six.iteritems(self.css):
                self.attrs['css'].setdefault(att, val)

    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs)
        self.patch_inline_style(final_attrs)
        return format_html('<{tag} {attrs}>{value}</{tag}>',
                           tag=self.tag,
                           value=value,
                           attrs=flatatt(final_attrs))

    def _patch_inline_style(self, attrs):
        self.tag = attrs.pop('tag', None) or self.tag
        css = attrs.pop('css', None) or self.css
        style = attrs.pop('style', None)
        style = style and styles2python(style)
        if style and css:
            style.update(css)
        elif style or css:
            style = style or css
        else:
            style = None
        return style

    def patch_inline_style(self, attrs):
        style = self._patch_inline_style(attrs)
        if style:
            attrs['style'] = python2styles(style)


class ImageWidget(TagWidget):
    tag = 'img'
    css = {
        'max-width': '80px',
        'max-height': '80px',
    }

    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs)
        self.patch_inline_style(final_attrs)
        if value:
            return format_html('<a target="_blank" href="{url}"><{tag} {attrs} src="{url}" /></a>',
                               tag=self.tag,
                               url=value.url,
                               attrs=flatatt(final_attrs))
        else:
            return ''


class Tag_H4(TagWidget):
    tag = 'h4'
    css = {
        'background': 'transparent',
    }


class Tag_P(TagWidget):
    tag = 'p'


class FieldWidget(forms.MultiWidget):
    name_widget = Tag_H4
    value_widget = Tag_P

    def __init__(self, attrs=None):
        widgets = []
        if attrs is None:
            attrs = {}

        widgets = [
            self.name_widget(attrs),
            self.value_widget(attrs),
            ]
        super(FieldWidget, self).__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def decompress(self, value):
        return value


class ImageFieldWidget(FieldWidget):
    value_widget = ImageWidget

    def format_output(self, rendered_widgets):
        return '<div>{0}</div>'.format(''.join(rendered_widgets))
