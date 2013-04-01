from sqlalchemy.orm.exc import NoResultFound

from warbase.model.ComputedValue import ComputedValue


class DbCache():

    def __init__(self, **kwargs):
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        self.session = kwargs['session']

    def _check_key(self, **kwargs):
        if 'key' not in kwargs:
            raise TypeError('key informations not provided')

        if not isinstance(kwargs['key'], str):
            raise AttributeError('key provided is not a string')

    def get(self, force=False, **kwargs):
        self._check_key(**kwargs)

        try:
            value = self.session.query(ComputedValue)\
                .filter(ComputedValue.key == kwargs['key'])\
                .one()
        except NoResultFound:
            return False

        if value.expired and not force:
            return False

        return value.value

    def set(self, **kwargs):
        self._check_key(**kwargs)

        if 'value' not in kwargs:
            raise TypeError('Value informations not provided')

        try:
            value = self.session.query(ComputedValue)\
                .filter(ComputedValue.key == kwargs['key'])\
                .one()
        except NoResultFound:
            value = ComputedValue()
            value.key = kwargs['key']

        value.expired = False
        value.value = kwargs['value']

        self.session.add(value)
        self.session.commit()

    def expire(self, **kwargs):
        self._check_key(**kwargs)

        if kwargs['key'][-1] == ':':
            values = self.session.query(ComputedValue)\
                .filter(ComputedValue.key.like(kwargs['key']+'%'))\
                .all()
        else:
            value = self.session.query(ComputedValue)\
                .filter(ComputedValue.key == kwargs['key'])\
                .one()
            values = [value]

        for a_val in values:
            a_val.expired = True
            self.session.add(a_val)

        self.session.commit()
