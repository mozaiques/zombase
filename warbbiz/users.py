
from warbmodel import User, Application
from . import BusinessWorker


class UsersBusiness(BusinessWorker):
    """Business object for users."""

    def _get_user(self, **kwargs):
        """Return a user given a user_id."""
        if 'user_id' not in kwargs:
            raise TypeError('user_id missing')

        user_id = kwargs['user_id']

        # Could raise NoResultFound or MultipleResultsFound
        user = self.ro_session.query(User.User)\
            .filter(User.User.id == user_id)\
            .one()

        return user

    def get_applications(self, **kwargs):
        """Return the formatted list of available apps for a user.

        Keyword arguments:
        user_id -- id of the user

        """
        user = self._get_user(**kwargs)

        # A user may have empty permissions
        if not user.permissions:
            return {}

        available_apps = {}

        apps = self.ro_session.query(Application.Application).all()

        for app in apps:
            if (app.name, app.min_permission) in user.permissions:
                available_apps[app.name] = {
                    'url': app.url,
                    'title': app.title,
                    'picto': app.picto}

        return available_apps
