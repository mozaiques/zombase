# -*- coding: utf-8 -*-
from datetime import datetime

from mozbase.util.database import db_method
from mozbase.model import Action

from . import AuthenticatedDataRepository


class ActionData(AuthenticatedDataRepository):
    """Data repository object for actions."""

    @db_method
    def create(self, **kwargs):
        """Create and insert an action in DB.

        Keyword arguments:
            see mozbase.model.Action.ActionSchema

        """
        add_datas = {'datetime': datetime.now(),
                     'created_by': self._user}
        kwargs = dict(kwargs.items() + add_datas.items())
        Action.ActionSchema(kwargs)

        action = Action.Action(**kwargs)
        self._dbsession.add(action)

        return action
