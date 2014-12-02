# -*- coding: utf-8 -*-
import inspect

from voluptuous import Schema

import six

from zombase.database import MetaBase


class RawWorker(object):
    """Deepest worker, root of all the interactions, only ensure there
    a sqlalchemy database session is available in `self._dbsession`."""

    def __init__(self, dbsession, check_sanity=True):
        if check_sanity and not hasattr(dbsession, 'cache'):
            raise ValueError(
                'Cache region not associated w/ database session.')

        self._dbsession = dbsession


class SupervisedWorker(RawWorker):
    """Worker intended to be used inside a foreman."""

    def __init__(self, foreman, foreman_name=None):
        RawWorker.__init__(self, foreman._dbsession)

        if not foreman_name:
            foreman_name = '_foreman'

        setattr(self, foreman_name, foreman)


class ObjectManagingWorker(SupervisedWorker):
    """Worker intended to be used inside a foreman, to take care of a
    specific sqlalchemy mapping.

    """

    def __init__(self, foreman=None, foreman_name=None, managed_object=None,
                 managed_object_name=None, id_type=None):
        SupervisedWorker.__init__(self, foreman, foreman_name)

        self._object = managed_object
        self._object_name = managed_object_name

        if id_type and id_type not in ('id', 'uuid'):
            raise AttributeError('Wrong `id_type`.')
        self._with_id = (id_type == 'id' or hasattr(self._object, 'id'))
        self._with_uuid = (id_type == 'uuid' or hasattr(self._object, 'uuid'))

    def _get(self, instance_id=None, instance=None, options=None):
        """Unified internal get for an object present in `instance_id`
        or `instance`, whose type is `self._object`.

        Keyword arguments:
            instance_id -- id (could be a "real" integer id or an uuid)
                           of the requested object
            instance -- object (internal use)
            options -- list of SQLA options to apply to the SQL request

        """
        if instance:
            if not isinstance(instance, self._object):
                raise AttributeError('`instance` doesn\'t match with the '
                                     'registered type.')
            return instance

        elif instance_id:
            if options is None:
                options = []
            query = self._dbsession.query(self._object)

            if self._with_id:
                query = query.filter(self._object.id == instance_id)
            elif self._with_uuid:
                query = query.filter(self._object.uuid == instance_id)
            else:
                raise StandardError('Can\'t determine id field.')

            return query.options(*options).one()

        raise TypeError('No criteria provided.')

    def _update(self, instance=None, schema=None, **kwargs):
        """Update an `instance`. Return False if there is no update and
        True otherwise.

        Do not raise error if too many arguments are given.

        Do not commit the database session.

        Keyword arguments:
            instance -- instance to update
            schema -- voluptuous schema to perform data validation

        """
        if not instance:
            raise TypeError('`instance` not provided.')

        if not schema:
            raise TypeError('`schema` not provided.')

        if not isinstance(schema, Schema):
            raise AttributeError('`schema` must be a voluptuous schema.')

        # Explicitely cast to string properties which come from schema
        # to deal with `voluptuous.Required` stuff.
        schema_keys = set([str(k) for k in schema.schema])

        obj_current_dict = {
            k: getattr(instance, k) for k in schema_keys
            if not getattr(instance, k) is None
        }
        obj_update_dict = obj_current_dict.copy()

        to_update = schema_keys.intersection(kwargs.keys())

        for item in to_update:
            obj_update_dict[item] = kwargs[item]

        obj_update_dict = schema(obj_update_dict)

        for item in to_update:
            setattr(instance, item, obj_update_dict[item])

        return obj_update_dict != obj_current_dict

    def _resolve_id(self, a_dict, schema, allow_none_id=False):
        """Return a dict fulfilled with the missing objects according to
        the given dict (in `a_dict`) and `schema`.

        Will fetch `instance` if `instance_id` (or `instance_uuid`) is
        in the dict keys, if `instance` is accepted by the schema and is
        supposed to be a sqlalchemy mapping.

        Additionnally if `instance_id` is not in the schema, it will be
        removed from the dict.

        If `allow_none_id` is true, passing `instance_id` with value
        'None' or '""' (empty string) will result in setting `instance`
        to 'None'.

        """
        _a_dict = a_dict.copy()

        for key, value in six.iteritems(schema.schema):
            if key in _a_dict.keys():
                continue

            if not inspect.isclass(value) or not issubclass(value, MetaBase):
                continue

            key_id = '{}_id'.format(key)
            key_uuid = '{}_uuid'.format(key)

            if key_id in a_dict and key_uuid in a_dict:
                raise Exception('`_resolve_id()` has been called with '
                                'both an `instance_id` and an '
                                '`instance_uuid`.')

            elif key_id in a_dict:
                val_id = _a_dict.pop(key_id)
                if not val_id and allow_none_id:
                    val = None

                else:
                    val = self._dbsession.query(value)\
                        .filter(value.id == val_id).one()

                _a_dict[str(key)] = val

            elif key_uuid in a_dict:
                val_uuid = _a_dict.pop(key_uuid)
                if not val_uuid and allow_none_id:
                    val = None

                else:
                    val = self._dbsession.query(value)\
                        .filter(value.uuid == val_uuid).one()

                _a_dict[str(key)] = val

        return _a_dict

    def get(self, instance_id=None, instance=None, options=None, **kwargs):
        """Unified external get for an object present in `instance_id`
        or `instance`.

        See also `ObjectManagingWorker._get()`.

        """
        if not instance_id and not instance:
            if not self._object_name:
                raise TypeError('No criteria provided.')

            instance_key = '{}'.format(self._object_name)
            if self._with_id:
                instance_id_key = '{}_id'.format(self._object_name)
            elif self._with_uuid:
                instance_id_key = '{}_uuid'.format(self._object_name)
            else:
                raise StandardError('Can\'t determine id field.')

            if instance_key in kwargs:
                instance = kwargs[instance_key]

            elif instance_id_key in kwargs:
                instance_id = kwargs[instance_id_key]

            else:
                raise TypeError('No criteria provided.')

        return self._get(instance_id, instance, options)

    def find(self):
        """Return a query to fetch multiple objects."""
        return self._dbsession.query(self._object)

    def serialize(self, items, **kwargs):
        """Transform the given list of `items` into an easily
        serializable list.

        Requires `self._serialize_one()` to be implemented. See
        `self.serialize_one()` for informations about `kwargs`.

        """
        return [self.serialize_one(item, **kwargs) for item in items]

    def _serialize_one(self, item):
        """Transform the given item into an easily serializable item.

        Most of the time it transforms a sqlalchemy mapped object into a
        dict with strings as keys and strings as values.

        A simple implementation would be:

            return {'id': item.id}

        Subclasses must implement this method to enable
        `self.serialize()` and `self.serialize_one()`.

        """
        raise NotImplementedError('Subclasses must implement '
                                  '`_serialize_one()`.')

    def serialize_one(self, item, **kwargs):
        """Leverage `self._serialize_one()` to provide a way to fully
        serialize a single item.

        Additional functions may be passed in `kwargs`, their results
        will be added to the serialized object once they have been
        executed with the item as single argument. Eg (with key=func):

            result[key] = func(item)

        """
        serialized = self._serialize_one(item)

        for key, function in six.iteritems(kwargs):
            serialized[key] = function(item)

        return serialized
