from datetime import datetime

from mozbase.util.database import db_method
from mozbase.model import Action

from . import DataRepository


class ActionsData(DataRepository):
    """DataRepository object for actions.

    Keyword arguments:
    session -- read and write SQLA-Session (required)
    user_id -- id of the user generating the action (*)
    user -- user generating the action (*)

    * at least one is required

    """

    def __init__(self, **kwargs):
        """Associate user with class instance."""
        DataRepository.__init__(self, **kwargs)
        self.user = self._get_user(**kwargs)

    @db_method()
    def create(self, **kwargs):
        """Create and insert an action in DB.

        Keyword arguments:
        see mozbase.model.Action.ActionSchema

        """
        add_datas = {'datetime': datetime.now(),
                     'created_by': self.user}
        kwargs = dict(kwargs.items() + add_datas.items())
        Action.ActionSchema(kwargs)  # Validate datas

        action = Action.Action(**kwargs)
        self.session.add(action)

        return action
