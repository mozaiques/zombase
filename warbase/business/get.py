from warbase.model import User, Application

from . import AbcBusinessWorker


class GetWorker(AbcBusinessWorker):

    def user(self, **kwargs):
        """Return a fully populated user given a user_id or a SQLA-User."""
        user = self._get_user(**kwargs)

        setattr(user, 'applications', self._user_applications(user))

        return user

    def computed_value(self, **kwargs):
        pass

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
