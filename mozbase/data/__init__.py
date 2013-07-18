# -*- coding: utf-8 -*-
from voluptuous import Schema


class RawDataRepository():
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
            raise TypeError('Patch requested on a object without `_patch_exports`')

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
        obj_current_dict = {str(k): getattr(instance, str(k)) for k in\
                            schema.schema if not getattr(instance, str(k)) is None}
        obj_update_dict = obj_current_dict.copy()

        to_update = [item for item in schema.schema if item in kwargs]

        for item in to_update:
            obj_update_dict[str(item)] = kwargs[item]

        schema(obj_update_dict)

        for item in to_update:
            setattr(instance, item, kwargs[item])

        if obj_update_dict == obj_current_dict:
            return False

        return instance


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
