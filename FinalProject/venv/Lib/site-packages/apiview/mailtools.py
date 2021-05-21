# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import six

from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import get_connection
from django import template
from django.template.loader import get_template


def mail(subject, to, body='', attachments=None, headers=None,
         cc=None, bcc=None, from_email=None, connection=None):
    '''
    normal mailer with EmailMessage
    '''
    if isinstance(to, six.string_types):
        to = [to]
    msg = EmailMultiAlternatives(
        subject=subject, body='', from_email=from_email, to=to, bcc=bcc,
        connection=connection, attachments=attachments, headers=headers, cc=cc)
    msg.attach_alternative(body, 'text/html')
    msg.send()


def render_to_mail(subject, to, context, content='', template_name=None, extend_context=True, **kwargs):
    '''
    extend mailer with template and contexts

    `context`:          dict like or Context objects to be rendered, or a list of them
    `content`:          template string content, ignored when `template` was set
    `template_name`:    template name to be load
    `extend_context`:   whether to extend context to match all mails to only if the `context` is a dict like object,
                        default true

    NOTE:
        the length of `context` should be equal with `to`
    '''
    if isinstance(to, six.string_types):
        to = [to]
    if isinstance(context, (dict, template.Context)):
        if extend_context:
            _context = []
            for x in range(len(to)):
                _context.append(context)
            context = _context
        else:
            context = [context]
    assert len(to) == len(context)

    if template_name:
        template_obj = get_template(template_name)
    else:
        template_obj = template.Template(content)

    connection = kwargs.pop('connection', get_connection())
    messages = []
    for _to, _context in zip(to, context):
        if not isinstance(_context, template.Context):
            _context = template.Context(_context)
        _body = template_obj.render(_context)
        msg = EmailMultiAlternatives(subject=subject, to=(_to, ), body='', **kwargs)
        msg.attach_alternative(_body, 'text/html')
        messages.append(msg)

    connection.send_messages(messages)
