# -*- coding: utf-8 -*-


class RawDataRepository():
    """Deepest object, only provide a database session and a cache
    interface.

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

    def patch(self, to_patch):
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
                prop.patch(to_patch_prop)
