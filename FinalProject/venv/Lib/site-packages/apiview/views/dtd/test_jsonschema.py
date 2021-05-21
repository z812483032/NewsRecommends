#! /usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals, absolute_import

import unittest

from .jsonschema import json2schema, gen_errors, flex_schema_by_errs


class TestJSONSchema(unittest.TestCase):
    def test_json2schema(self):
        self.assertEqual(json2schema([])['type'], 'array')
        self.assertEqual(json2schema({})['type'], 'object')
        self.assertEqual(json2schema({'a': 1.1})['properties']['a']['type'], 'number')
        self.assertEqual(json2schema({'a': 1})['properties']['a']['type'], 'integer')
        self.assertEqual(json2schema({'a': ''})['properties']['a']['type'], 'string')
        self.assertEqual(json2schema({'a': []})['properties']['a']['type'], 'array')
        self.assertEqual(json2schema({'a': {}})['properties']['a']['type'], 'object')

    def test_flex_schema_by_errs(self):
        data = {
            'string': 'value',
            'int': 1,
            'num': 1.0,
            'array': [1, 2, 3, 4],
            'object': {
                'sub_object': {
                    'sub_string': 'value',
                    'sub_int': 1,
                    'sub_num': 1.0,
                    'sub_array': [{'in_array': 'string'}, {'in_array': 1}, ],
                }},
            }

        schema = json2schema(data)

        # flex value
        data['int'] = 2
        self.assertEqual(next(gen_errors(data, schema)).validator, 'value')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex integer - number
        data['int'] = 2.0
        self.assertEqual(next(gen_errors(data, schema)).validator, 'type')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # the path generation
        data['object']['sub_object']['sub_int'] = 2
        self.assertEqual(next(gen_errors(data, schema)).validator, 'value')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex minItems and value
        data['array'] = [1, 2]
        self.assertEqual(len(list(gen_errors(data, schema))), 2)
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex maxItems
        data['array'] = [1, 2, 3, 4] * 2
        self.assertEqual(next(gen_errors(data, schema)).validator, 'maxItems')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex anyOf
        data['array'] = [1, 2, '5']
        self.assertEqual(next(gen_errors(data, schema)).validator, 'anyOf')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex flex_additionalProperties
        data['new_object'] = {'some': 'new object'}
        self.assertEqual(next(gen_errors(data, schema)).validator, 'additionalProperties')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))

        # flex complex types array
        data['object']['sub_object']['sub_array'] = [1, 2, '5', {'some': 'mixed value'}]
        self.assertEqual(next(gen_errors(data, schema)).validator, 'anyOf')
        flex_schema_by_errs(schema, list(gen_errors(data, schema)))
        self.assertFalse(list(gen_errors(data, schema)))


if __name__ == '__main__':
    unittest.main()
