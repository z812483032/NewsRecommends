# encoding: utf-8
from __future__ import absolute_import, unicode_literals


class CodeData(object):

    def __init__(self, code, tag, message):
        self.code = code
        self.message = message
        self.tag = tag

    def __str__(self):
        return str(self.code)

    def __eq__(self, other):
        if isinstance(other, CodeData):
            return other.code == self.code
        elif isinstance(other, type(self.code)):
            return other == self.code
        else:
            return super(CodeData, self).__eq__(other)

    def get_res_dict(self, **kwargs):
        ret = dict(kwargs)
        ret['code'] = self.code
        if 'message' not in ret:
            ret['message'] = self.message
        return ret


class Code(object):

    def __init__(self, code_define):
        codes = set()
        self._list = list()
        self._dict = dict()
        self._tags = list()
        for tag, code, message in code_define:
            assert code not in codes and not hasattr(self, tag)
            setattr(self, tag, CodeData(code, tag, message))
            codes.add(code)
            self._tags.append(tag)
            self._list.append((code, message))
            self._dict[code] = message

    def get_list(self):
        return self._list

    def get_dict(self):
        return self._dict

    def get_tags(self):
        return self._tags
