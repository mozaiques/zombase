# -*- coding: utf-8 -*-
from mozbase.data import InnerBoDataRepository


class DataRepository(InnerBoDataRepository):

    def __init__(self, bo=None):
        InnerBoDataRepository.__init__(self, bo=bo, bo_name='_mozbase')


class AuthenticatedDataRepository(DataRepository):
    """ABC for data repository objects with user informations."""

    def __init__(self, bo=None, user=None, user_id=None):
        """Associate database session, a get worker and a user to
        Repository.

        Argument:
            dbsession -- SQLAlchemy database session
            user_id -- id of the user (*)
            user -- user (*)

        * at least one is required

        """
        DataRepository.__init__(self, bo=bo)
        self._user = self._mozbase.user.get(user_id, user)
