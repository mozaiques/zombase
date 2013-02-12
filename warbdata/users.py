from warbmodel import User

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

    def _get_user(self, **kwargs):
        """Return a user given a user (other SQLA-Session) or a user_id."""
        if 'user' in kwargs:
            if not isinstance(kwargs['user'], User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            user = self.session.merge(kwargs['user'])

        elif 'user_id' in kwargs:
            user = self.session.query(User.User)\
                .filter(User.User.id == kwargs['user_id'])\
                .one()

        else:
            raise TypeError('User informations (user or user_id) not provided')

        return user

    def add_permission(self, **kwargs):
        """Add a permission to a user.

        Keyword arguments:
        permission -- valid permission tuple
        user -- warbmodel.User.User instance
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
