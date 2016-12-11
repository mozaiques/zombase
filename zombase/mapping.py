# -*- coding: utf-8 -*-
import inspect
import six

from voluptuous import Schema

from zombase.database import MetaBase


def update(sqla_obj, schema, ignore_keys=None, **kwargs):
    """Update an `instance`. Return False if there is no update and
    True otherwise.

    Do not raise error if too many arguments are given.

    Do not commit the database session.

    Keyword arguments:
        sqla_obj -- SQLAlchemy object to update
        schema -- voluptuous schema to perform data validation
        ignore_keys -- list of keys that will be ignored by this
                       function

    """
    if not isinstance(schema, Schema):
        raise AttributeError('`schema` must be a voluptuous schema.')

    if ignore_keys is None:
        ignore_keys = []

    # Explicitely cast to string properties which come from schema
    # to deal with `voluptuous.Required` stuff.
    schema_keys = set([str(k) for k in schema.schema if k not in ignore_keys])

    obj_current_dict = {
        k: getattr(sqla_obj, k) for k in schema_keys
        if not getattr(sqla_obj, k) is None
    }
    obj_update_dict = obj_current_dict.copy()

    to_update = schema_keys.intersection(kwargs.keys())

    for item in to_update:
        obj_update_dict[item] = kwargs[item]

    obj_update_dict = schema(obj_update_dict)

    for item in to_update:
        setattr(sqla_obj, item, obj_update_dict[item])

    return obj_update_dict != obj_current_dict


def resolve_id(build_query, a_dict, schema, allow_none_id=False):
    """Return a dict fulfilled with the missing objects according to
    the given dict (in `a_dict`) and `schema`.

    Will fetch `sqla_obj` if `sqla_obj_id` (or `sqla_obj_uuid`) is in
    the dict keys, if `sqla_obj` is accepted by the schema and is
    supposed to be a SQLAlchemy object.

    Additionnally if `sqla_obj_id` is not in the schema, it will be
    removed from the dict.

    If `allow_none_id` is true, passing `sqla_obj_id` with value
    'None' or '""' (empty string) will result in setting `sqla_obj`
    to 'None'.

    Arguments:
        build_query -- function which will be given a SQLAlchemy mapping
                       and must return an appropriate query
        a_dict -- base dictionnary
        schema -- reference voluptuous schema
        allow_none_id -- bool (see above)

    """
    _a_dict = a_dict.copy()

    for key, sqla_map in six.iteritems(schema.schema):
        if key in _a_dict.keys():
            continue

        if not inspect.isclass(sqla_map) or not issubclass(sqla_map, MetaBase):
            continue

        key_id = '{}_id'.format(key)
        key_uuid = '{}_uuid'.format(key)

        if key_id in a_dict and key_uuid in a_dict:
            raise Exception('`_resolve_id()` has been called with '
                            'both an `object_id` and an '
                            '`object_uuid`.')

        elif key_id in a_dict:
            val_id = _a_dict.pop(key_id)
            if not val_id and allow_none_id:
                val = None

            else:
                val = build_query(sqla_map).filter(sqla_map.id == val_id).one()

            _a_dict[str(key)] = val

        elif key_uuid in a_dict:
            val_uuid = _a_dict.pop(key_uuid)
            if not val_uuid and allow_none_id:
                val = None

            else:
                val = build_query(sqla_map)\
                    .filter(sqla_map.uuid == val_uuid).one()

            _a_dict[str(key)] = val

    return _a_dict
