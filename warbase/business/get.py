from warbase.model import User, Application

from . import AbcBusinessWorker


class GetWorker(AbcBusinessWorker):

    def user(self, user_id):
        """Return a user given a user_id."""
        # Could raise NoResultFound or MultipleResultsFound
        user = self.session.query(User.User)\
            .filter(User.User.id == user_id)\
            .one()

        setattr(user, 'applications', self._user_applications(user))

        return user

    def _user_applications(self, user):
        """Return the formatted list of available apps for a user."""
        # A user may have empty permissions
        if not user.permissions:
            return {}

        available_apps = {}

        apps = self.session.query(Application.Application).all()

        for app in apps:
            if (app.name, app.min_permission) in user.permissions:
                available_apps[app.name] = {
                    'url': app.url,
                    'title': app.title,
                    'picto': app.picto}

        return available_apps