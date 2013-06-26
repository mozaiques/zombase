# -*- coding: utf-8 -*-
from data import user, action


class BusinessWorker():

    def __init__(self, dbsession=None, **kwargs):
        """Init the business worker, create two interfaces for users and
        actions.

        Arguments:
            dbsession -- SQLA database session (patched with cache)

        Keyword arguments:
            user_id -- id of the user (*)
            user -- user (*)

        * at least one is required

        """
        self.user = user.UserData(dbsession=dbsession, **kwargs)

        # user informations must be in **kwargs.
        self.action = action.ActionData(dbsession=dbsession, **kwargs)
