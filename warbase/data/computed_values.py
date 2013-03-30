from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from warbase.model import ComputedValue
from . import DataRepository


class ComputedValuesData(DataRepository):

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

    def set(self, **kwargs):
        """Update or insert a computed value in DB.

        Keyword arguments:
        key -- string referencing the value
        target_id -- if of the target
        value -- value to set

        """
        if 'value' not in kwargs:
            raise TypeError('Value not provided')

        if not isinstance(kwargs['value'], float):
            raise AttributeError('value provided is not a float')

        try:
            kwargs['force_db'] = True
            computed_value = self._get_computed_value(**kwargs)
        except NoResultFound:
            computed_value = ComputedValue.ComputedValue(
                key=kwargs['key'],
                target_id=kwargs['target_id'])

        computed_value.expired = False
        computed_value.datetime = datetime.now()
        computed_value.value = kwargs['value']

        self.session.add(computed_value)

        self.session.commit()

        if self.cache:
            value = ComputedValue.CacheComputedValue(
                value=computed_value.value,
                key=kwargs['key'],
                target_id=kwargs['target_id'])
            self._set_in_cache(
                key=kwargs['key'],
                target_id=kwargs['target_id'],
                value=value)

        return computed_value

    def expire(self, **kwargs):
        """Expire a computed value (or a set of computed values) from DB.

        Keyword arguments:
        key -- string referencing the values (*)
        target_id -- if of the target

        """
        try:
            computed_values = self._get_computed_values(**kwargs)
        except NoResultFound:
            return

        for computed_value in computed_values:
            computed_value.expired = True
            self.session.add(computed_value)
            if self.cache:
                self._del_from_cache(
                    key=computed_value.key,
                    target_id=kwargs['target_id'])

        self.session.commit()

    def expire_key(self, **kwargs):
        """Expire all computed value with corresponding key from DB.

        Keyword arguments:
        key -- string referencing the values (*)

        """
        try:
            computed_values = self._get_computed_values_key(**kwargs)
        except NoResultFound:
            return

        for computed_value in computed_values:
            computed_value.expired = True
            self.session.add(computed_value)
            if self.cache:
                self._del_from_cache(
                    key=computed_value.key,
                    target_id=computed_value.target_id)

        self.session.commit()
