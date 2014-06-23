# -*- coding: utf-8 -*-
from mozbase.data import RawDataRepository
from mozbase.data.action import ActionData
from mozbase.data.user import UserData


class BusinessObject(RawDataRepository):

    def __init__(self, dbsession=None, user_id=None, user=None):
        """Init the business object, create two interfaces for users and
        actions.

        Arguments:
            dbsession -- SQLA database session (patched with cache)
            user_id -- id of the user (*)
            user -- user (*)

        * at least one is required

        """
        RawDataRepository.__init__(self, dbsession)
        self.user = UserData(self)
        self.action = ActionData(self, user_id=user_id, user=user)
