# encoding: utf-8
from __future__ import absolute_import, unicode_literals


class DTDError(Exception):
    """Base Error of this Module"""


class DTDSchemaError(DTDError):
    """Raise when translating data to DTD failed"""
    def __init__(self, message, instance, path, cause=None):
        self.message = message
        self.instance = instance
        self.path = path
        self.cause = cause


class DTDProcessError(DTDError):
    """Raise when processing data or schema failed"""
    def __init__(self, message, validator, instance, schema, path, schema_path, cause=None):
        self.message = message
        self.validator = validator
        self.instance = instance
        self.schema = schema
        self.path = path
        self.schema_path = schema_path
        self.cause = cause

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.message)

    def __unicode__(self):
        return self.message


class DTDValidationError(DTDProcessError):
    """Raise when validating data failed"""


class DTDFlexError(DTDProcessError):
    """Raise when flexing schema failed"""
