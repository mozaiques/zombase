from mozbase.util.database import db_method
from mozbase.model import User

from . import DataRepository


class UserData(DataRepository):
    """DataRepository object for users."""

    def get(self, **kwargs):
        """Return a fully populated user given a user_id or a SQLA-User."""
        return self._get.user(**kwargs)

    @db_method()
    def create(self, **kwargs):
        """Create and insert a user in DB.

        Keyword arguments:
        see warbmodel.User.UserSchema

        """
        # Validate datas
        User.UserSchema(kwargs)

        user = User.User(**kwargs)
        self._dbsession.add(user)

        return user

    @db_method()
    def add_permission(self, **kwargs):
        """Add a permission to a user.

        Keyword arguments:
        permission -- valid permission tuple
        user -- warbase.model.User.User instance
        user_id -- id of the user

        """
        user = self._get.user(**kwargs)

        if 'permission' not in kwargs:
            raise TypeError('permission missing')

        User.PermissionSchema(kwargs['permission'])

        if not user.permissions:
            user.permissions = [kwargs['permission']]

        if kwargs['permission'] not in user.permissions:
            user.permissions.append(kwargs['permission'])

        return user
