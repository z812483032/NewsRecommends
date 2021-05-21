# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import types
import logging

CALLER_KEY = '_caller_'


class ManualCallerLogger(logging.Logger):
    """
    Allow to overwrite LogRecord object's attributes with extra
    """
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if extra and CALLER_KEY in extra:
            caller = extra.get(CALLER_KEY)
            if isinstance(caller, types.FunctionType):
                f_code = caller.func_code
                fn = f_code.co_filename
                lno = f_code.co_firstlineno
                func = f_code.co_name
            elif isinstance(caller, types.MethodType):
                f_code = caller.im_func.func_code
                fn = f_code.co_filename
                lno = f_code.co_firstlineno
                if isinstance(caller.im_self, types.ClassType):
                    func = caller.im_self.__name__
                else:
                    func = caller.im_class.__name__

        return super(ManualCallerLogger, self).makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
