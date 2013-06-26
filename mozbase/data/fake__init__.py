# -*- coding: utf-8 -*-
from mozbase.data import RawDataRepository
from mozbase.data.subworker.get import GetWorker


class DataRepository(RawDataRepository):
    """ABC for data repository objects."""

    def __init__(self, dbsession=None, **kwargs):
        """Associate database session and a get subworker.

        Argument:
            dbsession -- SQLAlchemy database session

        """
        RawDataRepository.__init__(self, dbsession)
        self._get = GetWorker(dbsession=dbsession)


class AuthenticatedDataRepository(DataRepository):
    """ABC for data repository objects with user informations."""

    def __init__(self, dbsession=None, user=None, user_id=None, **kwargs):
        """Associate database session, a get worker and a user to
        Repository.

        Argument:
            dbsession -- SQLAlchemy database session
            user -- User object

        * at least one is required

        """
        DataRepository.__init__(self, dbsession)
        self._user = self._get.user(user_id, user)
