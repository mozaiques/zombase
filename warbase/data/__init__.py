from sqlalchemy.orm.session import Session as SQLA_Session
from sqlalchemy.orm.exc import NoResultFound

from warbase.model import User, ComputedValue


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def __init__(self, **kwargs):
        """Init a SQLA-Session."""
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        # Scoped session does not inherit from Session ... Not possible yet.
        # if not isinstance(kwargs['session'], SQLA_Session):
        #     raise AttributeError('session provided is not a SQLA-Session')

        self.session = kwargs['session']

    def _get_user(self, **kwargs):
        """Return a user given a user (other SQLA-Session) or a user_id."""
        if 'user' in kwargs:
            if not isinstance(kwargs['user'], User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            return self.session.merge(kwargs['user'])

        elif 'user_id' in kwargs:
            return self.session.query(User.User)\
                .filter(User.User.id == kwargs['user_id'])\
                .one()

        else:
            raise TypeError('User informations (user or user_id) not provided')

    def _get_computed_value(self, **kwargs):
        """Return an computed value given a key and a target_id"""
        if 'key' not in kwargs or 'target_id' not in kwargs:
            raise TypeError('Value informations not provided')
        
        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

        if not isinstance(kwargs['target_id'], int):
            raise AttributeError('target_id provided is not an integer')

        return self.session.query(ComputedValue.ComputedValue)\
            .filter(ComputedValue.ComputedValue.key == kwargs['key'])\
            .filter(ComputedValue.ComputedValue.target_id == kwargs['target_id'])\
            .one()

    def _get_computed_values(self, **kwargs):
        """Return a list computed value given a key prefix and a target_id"""
        if 'key' not in kwargs or 'target_id' not in kwargs:
            raise TypeError('Value informations not provided')
        
        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

        if not isinstance(kwargs['target_id'], int):
            raise AttributeError('target_id provided is not an integer')

        if kwargs['key'][-1] == ':':
            computed_values = self.session.query(ComputedValue.ComputedValue)\
                .filter(ComputedValue.ComputedValue.key.like(kwargs['key']+'%'))\
                .filter(ComputedValue.ComputedValue.target_id == kwargs['target_id'])\
                .all()

        else:
            computed_value = self.session.query(ComputedValue.ComputedValue)\
            .filter(ComputedValue.ComputedValue.key == kwargs['key'])\
            .filter(ComputedValue.ComputedValue.target_id == kwargs['target_id'])\
            .one()
            computed_values = [computed_value]
        
        return computed_values
