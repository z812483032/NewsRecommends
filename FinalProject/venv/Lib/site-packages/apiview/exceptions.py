# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from .err_code import ErrCode


class CustomError(ValueError):
    '''客户操作错误，用于在系统流程设计不完善时，处理客户无意提交的错误请求'''
    def __init__(self, errcode=ErrCode.ERR_COMMON_BAD_PARAM, **kwargs):
        self.code = errcode
        self.kwargs = kwargs
        message = self.kwargs.get('message', errcode.message)
        super(CustomError, self).__init__(message)

    def get_res_dict(self):
        return self.code.get_res_dict(**self.kwargs)
