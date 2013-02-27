from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from warbase.model import ComputedValue
from . import DataRepository


class ComputedValuesData(DataRepository):

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
            computed_value = self._get_computed_value(**kwargs)
        except NoResultFound:
            computed_value = ComputedValue.ComputedValue(
                key=kwargs['key'],
                target_id=kwargs['target_id'])

        computed_value.expired = False
        computed_value.datetime = datetime.now()
        computed_value.value = kwargs['value']

        self.session.add(computed_value)

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
            return False

        for computed_value in computed_values:
            computed_value.expired = True
            self.session.add(computed_value)

        self.session.flush()
        return True
