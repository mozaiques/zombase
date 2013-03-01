from datetime import datetime

from warbase.model import Action

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

    def create(self, **kwargs):
        """Create and insert an action in DB.

        Keyword arguments:
        see warbase.model.Action.ActionSchema

        """
        add_datas = {'datetime': datetime.now(),
                     'created_by': self.user}
        kwargs = dict(kwargs.items() + add_datas.items())
        action_schema = Action.ActionSchema(kwargs)  # Validate datas

        action = Action.Action(**kwargs)
        self.session.add(action)

        # To get a full action to return (get a working id)
        self.session.flush()

        return action