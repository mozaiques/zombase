from datetime import datetime

from warbmodel import Action

from . import DataRepository


class ActionsData(DataRepository):
    """DataRepository object for actions.

    Keyword arguments:
    session -- read and write SQLA-Session (required)
    user_id -- id of the user using the application (*)
    user -- user using the application (*)

    * at least one is required

    """

    def __init__(self, **kwargs):
        """Associate user and application with class instance."""
        DataRepository.__init__(self, **kwargs)
        self.user = self._get_user(**kwargs)
        self.application = self._get_application(**kwargs)

    def create(self, **kwargs):
        """Create and insert an application in DB.

        Keyword arguments:
        see warbmodel.Action.ApplicationSchema

        """
        add_datas = {'datetime': datetime.now(),
                     'created_by': self.user,
                     'application': self.application}
        kwargs = dict(kwargs.items() + add_datas.items())
        action_schema = Action.ActionSchema(kwargs)  # Validate datas

        action = Action.Action(**kwargs)
        self.session.add(action)

        # To get a full application to return (get a working id)
        self.session.flush()

        return action
