# -*- coding: utf-8 -*-
from mozbase.model import User

from mozbase.data import RawDataRepository


class GetWorker(RawDataRepository):
    """Internal object to perform 'raw' gets."""

    def user(self, user_id=None, user=None):
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
