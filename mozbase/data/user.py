# -*- coding: utf-8 -*-
from mozbase.model import User
from mozbase.data.fake__init__ import DataRepository
from mozbase.util.database import db_method


class UserData(DataRepository):
    """Data repository object for users."""

    def get(self, user_id=None, user=None):
        """Return a user given a user (other SQLA-Session) or a user_id.

        Argument:
            user_id -- id of the user (*)
            user -- SQLA-User (instance of mozbase.model.User.User) (*)

        * at least one is required

        """
        if user:
            if not isinstance(user, User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            return self._dbsession.merge(user)

        elif user_id:
            return self._dbsession.query(User.User)\
                .filter(User.User.id == user_id)\
                .one()

        else:
            raise TypeError('User informations (user or user_id) not provided')

    @db_method
    def create(self, **kwargs):
        """Create and insert a user in DB.

        Keyword arguments:
            see mozbase.model.User.UserSchema

        """
        # Validate datas
        User.UserSchema(kwargs)

        user = User.User(**kwargs)
        self._dbsession.add(user)

        return user

    @db_method
    def add_permission(self, user_id=None, user=None, permission=None,
                       **kwargs):
        """Add a permission to a user.

        Arguments:
            user_id -- id of the user (*)
            user -- mozbase.model.User.User instance (*)
            permission -- a permission (a string in this implementation)

        * at least one is required

        """
        user = self.get(user_id, user)

        if not permission:
            raise TypeError('permission missing')

        User.PermissionSchema(permission)

        if not user.permissions:
            user.permissions = [permission]

        if permission not in user.permissions:
            user.permissions.append(permission)

        return user
