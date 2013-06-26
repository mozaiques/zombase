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
