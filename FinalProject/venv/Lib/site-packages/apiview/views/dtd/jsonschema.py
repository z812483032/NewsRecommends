# encoding: utf-8
from __future__ import absolute_import, unicode_literals

# JSONSCHEMA is a simple and well functional wrapped JSON validator
from jsonschema import Draft4Validator, ValidationError
from jsonschema.validators import create
from jsonschema.compat import iteritems
from jsonschema._utils import find_additional_properties

from .exceptions import DTDSchemaError, DTDValidationError, DTDFlexError

VALUEED_TYPES = ('boolean', 'integer', 'null', 'number', 'string')


def _value(validator, value, instance, schema):
    if instance != value:
        yield ValidationError('%s is not the value %s' % (instance, value))


# add `value` schema to validate equality conveniently
draft4_schema_ext = Draft4Validator.META_SCHEMA.copy()
draft4_schema_ext['properties']['value'] = {
    'oneOf': [
        {'type': 'string'},
        {'type': 'number'},
        {'type': 'array'},
    ],
}

draft4_validators_ext = Draft4Validator.VALIDATORS.copy()
draft4_validators_ext['value'] = _value

ExtDraft4Validator = create(draft4_schema_ext, draft4_validators_ext)

default_validator = ExtDraft4Validator({})

# reverse type map from Python to JSON schema
reversed_types = {}
for schema, types in iteritems(ExtDraft4Validator.DEFAULT_TYPES):
    if isinstance(types, (tuple, list)):
        for type_ in types:
            reversed_types[type_] = schema
    else:
        reversed_types[types] = schema

DEFAULT_SCHEMA_NODE = {}


def get_subnode(root, path):
    node = root
    for step in path:
        node = node[step]
    return node


def get_subpath(name, path):
    sub_path = []
    sub_path.extend(path)
    if name is not None:
        sub_path.append(name)
    return sub_path


def json2schema(node, name=None, path=(), check_value=True):
    """Return a strict validation schema for the given JSON node"""
    node_type = type(node)
    if node_type not in reversed_types:
        for type_, schemta in iteritems(reversed_types):
            if isinstance(node, type_):
                reversed_types[node_type] = schemta
                break
        else:
            raise DTDSchemaError(
                "Unexpected type %s at path %s" % (node_type, path),
                instance=node,
                path=path)

    schema = DEFAULT_SCHEMA_NODE.copy()
    schema['type'] = reversed_types[node_type]
    if schema['type'] == 'array':
        length = len(node)
        if length:
            sub_schemas = []
            sub_path = get_subpath(name, path)
            sub_types = set()
            for sub_node in node:
                sub_schema = json2schema(sub_node, path=sub_path, check_value=False)
                sub_types.add(sub_schema['type'])
                sub_schemas.append(sub_schema)
            if not sub_types.intersection(['array', 'object']):
                if check_value:
                    schema['value'] = node
                sub_schemas = [{'type': _type} for _type in sub_types]
            schema['items'] = {'anyOf': sub_schemas}
            schema['maxItems'] = schema['minItems'] = length
        else:
            schema['value'] = node
            schema['minItems'] = 0
            schema['additionalItems'] = False
    elif schema['type'] == 'object':
        sub_items = []
        sub_path = get_subpath(name, path)
        for sub_name, sub_node in iteritems(node):
            sub_items.append((sub_name, json2schema(sub_node, sub_name, sub_path, check_value=check_value)))
        if sub_items:
            properties = {}
            for sub_name, sub_schema in sub_items:
                properties[sub_name] = sub_schema
            schema['properties'] = properties
            schema['required'] = list(properties)
        schema['additionalProperties'] = False
    elif check_value:
        schema['value'] = node
    return schema


def gen_errors(data, schema, valudator=None):
    """Return an errors' generation"""
    valudator = valudator or default_validator
    for err in valudator.iter_errors(data, schema):
        yield DTDValidationError(
                message=err.message,
                validator=err.validator,
                instance=err.instance,
                schema=err.schema,
                path=err.absolute_path,
                schema_path=err.absolute_schema_path,
                cause=err.cause,
            )


def validate(data, schema, validator=None):
    for err in gen_errors(data, schema, validator):
        raise err


def flex_schema_by_err(schema, err):
    """Flex schema according to the DTDValidationError with handlers defined in this module"""
    handler = globals().get('flex_' + err.validator, None)
    if handler is None:
        raise DTDFlexError(
                'Unhandled validator: %s' % err.validator,
                # message=err.message,
                validator=err.validator,
                instance=err.instance,
                schema=err.schema,
                path=err.path,
                schema_path=err.schema_path,
                cause=err.cause,
            )

    schema_node = get_subnode(schema, list(err.schema_path)[:-1])
    handler(schema_node, err)


def flex_schema_by_errs(schema, errs):
    """Flex schema according to the DTDValidationErrors"""
    for err in errs:
        flex_schema_by_err(schema, err)


def flex_type(schema, err):
    if schema['type'] == 'integer':
        schema['type'] = 'number'
    else:
        raise DTDFlexError(
                'Could not flex type: %s' % schema['type'],
                # message=err.message,
                validator=err.validator,
                instance=err.instance,
                schema=err.schema,
                path=err.path,
                schema_path=err.schema_path,
                cause=err.cause,
            )


def flex_required(schema, err):
    required = set(schema['required']).intersection(err.instance)
    schema['required'] = list(required)


def flex_minItems(schema, err):
    del schema['minItems']


def flex_maxItems(schema, err):
    del schema['maxItems']


def flex_value(schema, err):
    del schema['value']


def flex_additionalProperties(schema, err):
    extras = find_additional_properties(err.instance, err.schema)
    for extra in extras:
        schema['properties'][extra] = json2schema(err.instance[extra], extra, err.path)


def flex_anyOf(schema, err):
    sub_schema = json2schema(err.instance, err.path, check_value=False)
    schema['anyOf'].append(sub_schema)
    sub_types = set([item['type'] for item in schema['anyOf']])
    if not sub_types.intersection(['array', 'object']):
        schema['anyOf'] = [{'type': _type} for _type in sub_types]
