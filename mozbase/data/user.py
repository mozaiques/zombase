# -*- coding: utf-8 -*-
from mozbase.util.database import db_method
from mozbase.model import User

from . import DataRepository


class UserData(DataRepository):
    """Data repository object for users."""

    def get(self, user_id=None, user=None, **kwargs):
        """Return a fully populated user given a user_id or a SQLA-User."""
        return self._get.user(user_id, user)

    @db_method()
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

    @db_method()
    def add_permission(self, user_id=None, user=None, permission=None,
                       **kwargs):
        """Add a permission to a user.

        Arguments:
            user_id -- id of the user (*)
            user -- mozbase.model.User.User instance (*)
            permission -- a permission (can be a string, a tuple, ...)

        * at least one is required

        """
        user = self._get.user(user_id, user)

        if not permission:
            raise TypeError('permission missing')

        User.PermissionSchema(permission)

        if not user.permissions:
            user.permissions = [ permission ]

        if permission not in user.permissions:
            user.permissions.append(permission)

        return user
