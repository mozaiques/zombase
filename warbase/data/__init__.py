from sqlalchemy.orm.exc import NoResultFound

from warbase.model import User, ComputedValue


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    Handle cache interaction.

    """

    def __init__(self, **kwargs):
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        self.session = kwargs['session']

        if 'cache' in kwargs:
            self.cache = kwargs['cache']
        else:
            self.cache = False

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

    def _cache_key(self, **kwargs):
        """Return a cache key."""
        return ':'.join([kwargs['key'], str(kwargs['target_id'])])

    def _get_from_cache(self, **kwargs):
        """Get a value from the cache.

        Keyword arguments:
        key -- key of the value
        target_id -- id of the target

        """
        return self.cache.get(self._cache_key(**kwargs))

    def _set_in_cache(self, **kwargs):
        """Set a value in the cache.

        Keyword arguments:
        key -- key of the value
        target_id -- id of the target
        value -- value to set

        """
        self.cache.set(self._cache_key(**kwargs), kwargs['value'])

    def _del_from_cache(self, **kwargs):
        """Delete a value from the cache.

        Keyword arguments:
        key -- key of the value
        target_id -- id of the target

        """
        self.cache.delete(self._cache_key(**kwargs))

    def _get_computed_value(self, force_db=False, **kwargs):
        """Return an computed value given a key and a target_id. Work with
        cache

        Keyword arguments:
        key -- key of the value
        target_id -- id of the target
        force_db -- wether to force a check in DB or not

        """
        if 'key' not in kwargs or 'target_id' not in kwargs:
            raise TypeError('Value informations not provided')

        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

        if not isinstance(kwargs['target_id'], int):
            raise AttributeError('target_id provided is not an integer')

        # Try to get the value in the cache
        if self.cache and not force_db:
            value = self._get_from_cache(
                key=kwargs['key'],
                target_id=kwargs['target_id'])
            if value:
                return value

        value = self.session.query(ComputedValue.ComputedValue)\
            .filter(ComputedValue.ComputedValue.key == kwargs['key'])\
            .filter(ComputedValue.ComputedValue.target_id == kwargs['target_id'])\
            .one()

        if value.expired:
            if force_db:
                return value
            raise NoResultFound

        # Add the value to the cache
        if self.cache:
            self._set_in_cache(
                key=kwargs['key'],
                target_id=kwargs['target_id'],
                value=value)

        return value

    def _get_computed_values(self, **kwargs):
        """Return a list of computed value given a key prefix and a target_id.
        Do not work with cache

        """
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
                .filter(ComputedValue.ComputedValue.expired == False)\
                .all()

        else:
            computed_value = self._get_computed_value(force_db=True, **kwargs)
            computed_values = [computed_value]

        return computed_values

    def _get_computed_values_key(self, **kwargs):
        """Return a list computed value given a key prefix. Do not work with
        cache.

        """
        if 'key' not in kwargs:
            raise TypeError('Value informations not provided')

        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

        computed_values = self.session.query(ComputedValue.ComputedValue)\
            .filter(ComputedValue.ComputedValue.key.like(kwargs['key']+'%'))\
            .filter(ComputedValue.ComputedValue.expired == False)\
            .all()

        return computed_values
