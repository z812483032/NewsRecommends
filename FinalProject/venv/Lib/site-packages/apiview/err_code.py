# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.conf import settings

from .code import Code


CodeDefine = (
    ('SUCCESS',                     0,      '返回成功'),

    ('ERR_UNKOWN',                  -1,     '未知错误'),
    ('ERR_SYS_ERROR',               -2,     '服务异常'),

    ('ERR_COMMON_BAD_PARAM',        -11,    '参数错误'),
    ('ERR_COMMON_BAD_FORMAT',       -12,    '格式错误'),
    ('ERR_COMMON_PERMISSION',       -13,    '权限错误'),
)

ErrCode = Code(CodeDefine + getattr(settings, "ERROR_CODE_DEFINE", ()))
