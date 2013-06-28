# -*- coding: utf-8 -*-
import mozbase.data


class BusinessWorker(mozbase.data.RawDataRepository):

    def __init__(self, dbsession=None, user_id=None, user=None):
        """Init the business worker, create two interfaces for users and
        actions.

        Arguments:
            dbsession -- SQLA database session (patched with cache)
            user_id -- id of the user (*)
            user -- user (*)

        * at least one is required

        """
        mozbase.data.RawDataRepository.__init__(self, dbsession)
        self.user = mozbase.data.user.UserData(dbsession=dbsession)

        # user informations must be in **kwargs.
        self.action = mozbase.data.action.ActionData(dbsession=dbsession, user_id=user_id, user=user)
