from sqlalchemy.orm.session import Session as SQLA_Session
from sqlalchemy.orm.exc import NoResultFound

from warbmodel import User


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def __init__(self, **kwargs):
        """Init a SQLA-Session."""
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        if not isinstance(kwargs['session'], SQLA_Session):
            raise AttributeError('session provided is not a SQLA-Session')

        self.session = kwargs['session']

    def _get_user(self, **kwargs):
        """Return a user given a user (other SQLA-Session) or a user_id."""
        if 'user' in kwargs:
            if not isinstance(kwargs['user'], User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            user = self.session.merge(kwargs['user'])

        elif 'user_id' in kwargs:
            try:
                user = self.session.query(User.User)\
                    .filter(User.User.id == kwargs['user_id'])\
                    .one()
            except NoResultFound:
                raise AttributeError('user_id provided doesn\'t exist')

        else:
            raise TypeError('User informations (user or user_id) not provided')

        return user
