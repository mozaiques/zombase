from warbase.model import User

from . import DataRepository


class UsersData(DataRepository):
    """DataRepository object for users."""

    def create(self, **kwargs):
        """Create and insert an application in DB.

        Keyword arguments:
        see warbmodel.User.UserSchema

        """
        # Validate datas
        user_schema = User.UserSchema(kwargs)

        user = User.User(**kwargs)
        self.session.add(user)

        # To get a full user to return (get a working id)
        self.session.flush()

        return user

    def add_permission(self, **kwargs):
        """Add a permission to a user.

        Keyword arguments:
        permission -- valid permission tuple
        user -- warbase.model.User.User instance
        user_id -- id of the user

        """
        user = self._get_user(**kwargs)

        if 'permission' not in kwargs:
            raise TypeError('permission missing')

        permission_schema = User.PermissionSchema(kwargs['permission'])

        if not user.permissions:
            user.permissions = [kwargs['permission']]

        if kwargs['permission'] not in user.permissions:
            user.permissions.append(kwargs['permission'])

        self.session.flush()
        return user
