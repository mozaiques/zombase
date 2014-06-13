# -*- coding: utf-8 -*-
import inspect

from voluptuous import Schema

from mozbase.util.database import MetaBase


class RawDataRepository(object):
    """Deepest object, only provide a database session (with a cache
    interface).

    """

    def __init__(self, dbsession=None):
        """Associate database session.

        Argument:
            dbsession -- SQLAlchemy database session patched with a
                         cache

        """
        if not dbsession:
            raise TypeError('Database session not provided')

        if not hasattr(dbsession, 'cache'):
            raise TypeError('Cache region not associated w/ database session')

        self._dbsession = dbsession

    def _patch(self, to_patch):
        """Insert properties listed in `_patch_exports` into the given
        object.

        Argument:
            to_patch -- Object in which properties will be inserted

        """

        if not hasattr(self, '_patch_exports'):
            raise TypeError(
                'Patch requested on a object without `_patch_exports`')

        for prop_key in self._patch_exports:
            prop = getattr(self, prop_key)

            # Patched object doesn't have the property, just set it
            if not hasattr(to_patch, prop_key):
                setattr(to_patch, prop_key, prop)
                continue

            # We delegate to the children
            if hasattr(prop, '_patch_exports'):
                to_patch_prop = getattr(to_patch, prop_key)
                prop._patch(to_patch_prop)


class InnerBoDataRepository(RawDataRepository):
    """DataRepository intended to be used inside a business object"""

    def __init__(self, bo=None, bo_name=None):
        """Init a DataRepository object.

        Keyword arguments:
            bo -- parent business object
            bo_name -- name that will be given to the parent business
                       object reference

        """
        if not bo:
            raise TypeError('`bo` not provided')

        if not hasattr(bo, '_dbsession'):
            raise TypeError('Database session not associated w/ provided bo')

        if not bo_name:
            bo_name = '_bo'

        setattr(self, bo_name, bo)
        RawDataRepository.__init__(self, bo._dbsession)


class ObjectManagingDataRepository(InnerBoDataRepository):
    """DataRepository intended to be used inside a business object, to
    take care of a specific objects (instances of a SQLA-class).

    """

    def __init__(self, bo=None, bo_name=None, managed_object=None,
        managed_object_name=None):
        """Init a DataRepository object.

        Keyword arguments:
            bo & bo_name -- see InnerBoDataRepository
            managed_object -- object (SQLA-class) that will be managed
                              (eg: mozbase.model.User.User)
            managed_object_name -- name of the object that will be
                                   managed (eg: 'user')

        """
        InnerBoDataRepository.__init__(self, bo, bo_name)
        self._managed_object = managed_object
        self._managed_object_name = managed_object_name

    def _get(self, instance_id=None, instance=None, type=None):
        """Unified internal get for an object present in `instance_id`
        or `instance`, whose type is `type`

        Keyword arguments:
            instance_id -- id of the requested object
            instance -- object (internal use)
            type -- type of the expected object. will try to use
                    `self._managed_object` if not given.

        """
        if type is None:
            if not self._managed_object:
                raise TypeError('`type` not provided')
            type = self._managed_object

        if instance:
            if not isinstance(instance, type):
                raise AttributeError(
                    '`instance` doesn\'t match with the given type')
            return instance

        elif instance_id:
            return self._dbsession.query(type)\
                .filter(type.id == instance_id)\
                .one()

        raise TypeError('No criteria provided')

    def _update(self, instance=None, schema=None, **kwargs):
        """Update an instance. Return False if there is no update or the
        updated instance.

        Do not raise error if too many arguments are given.

        Do not commit the session.

        Keyword arguments:
            instance -- instance to update
            schema -- schema (voluptuous) to perform data validation

        """
        if not instance:
            raise TypeError('instance not provided')

        if not schema:
            raise TypeError('schema not provided')

        if not isinstance(schema, Schema):
            raise AttributeError('schema must be a voluptuous schema')

        # Explicitely cast to string properties which come from schema
        # to deal with Required stuff.
        obj_current_dict = {
            str(k): getattr(instance, str(k)) for k in schema.schema
            if not getattr(instance, str(k)) is None
        }
        obj_update_dict = obj_current_dict.copy()

        to_update = [item for item in schema.schema if str(item) in kwargs]

        for item in to_update:
            obj_update_dict[str(item)] = kwargs[str(item)]

        obj_update_dict = schema(obj_update_dict)

        for item in to_update:
            setattr(instance, str(item), obj_update_dict[str(item)])

        if obj_update_dict == obj_current_dict:
            return False

        return instance

    def _resolve_id(self, a_dict, schema, allow_none_id=False):
        """Return a dict fulfilled with the missing objects according to
        the given dict and schema.

        Will fetch `instance` if `instance_id` is in the dict keys, if
        `instance` is accepted by the schema and is supposed to be a
        SQLA-object.

        Additionnally if `instance_id` is not in the schema, it will be
        removed from the dict.

        If `allow_none_id` is true, passing `instance_id` with value
        'None' or '""' (empty string) will result in setting `instance`
        to 'None'.

        """
        _a_dict = a_dict.copy()

        for key, v in schema.schema.iteritems():
            if not key in _a_dict.keys()\
                    and inspect.isclass(v)\
                    and issubclass(v, MetaBase):
                key_id = '{}_id'.format(key)
                if key_id in _a_dict.keys():
                    val_id = _a_dict.get(key_id)
                    if not val_id and allow_none_id:
                        val = None
                    else:
                        val = self._dbsession.query(v)\
                            .filter(v.id == val_id).one()
                    _a_dict[str(key)] = val
                    if not key_id in schema.schema:
                        _a_dict.pop(key_id)

        return _a_dict

    def get(self, instance_id=None, instance=None, type=None, **kwargs):
        """Unified external get for an object present in `instance_id`
        or `instance`, whose type is `type`.

        See also `DataRepository._get()`.

        """
        if not instance_id and not instance:
            if not self._managed_object_name:
                raise TypeError('No criteria provided')

            instance_key = '{}'.format(self._managed_object_name)
            instance_id_key = '{}_id'.format(self._managed_object_name)

            if instance_key in kwargs:
                instance = kwargs[instance_key]

            elif instance_id_key in kwargs:
                instance_id = kwargs[instance_id_key]

        return self._get(instance_id, instance, type)

    def find(self, type=None):
        """Return a query to fetch multiple objects."""
        return self._dbsession.query(self._managed_object)

    def serialize(self, items, **kwargs):
        """Transform the given list of items into an easily serializable
        list.

        Requires `self.serialize_one()` to be implemented. See this
        method and `self._serialize_one()` for informations about
        `kwargs`.

        """
        serialized = []
        for item in items:
            serialized.append(self.serialize_one(item, **kwargs))
        return serialized

    def _serialize_one(self, serialized, item, **kwargs):
        """Execute functions in `kwargs` with `item` as argument and add
        the results to `serialized`.

        See `self._serialize_one()` for more explanations.

        """
        for key in kwargs:
            serialized[key] = kwargs[key](item)

        return serialized

    def serialize_one(self, item, **kwargs):
        """Transform the given item into an easily serializable item.

        Most of the time it transforms a SQLA-object into a dict with
        strings as keys and strings as values.

        Additional functions may be passed in `kwargs`, their results
        will be added to the serialized object once they have been
        executed with the item as single argument. Eg (with key=func):

            result[key] = func(item)

        A simple implementation would be:

            serialized = {'id': item.id}
            return self._serialize_one(serialized, item, **kwargs)

        Subclasses must implement this method to enable
        `self.serialize()`.

        """
        raise NotImplementedError
