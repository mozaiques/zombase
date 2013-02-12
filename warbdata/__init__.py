from sqlalchemy.orm.session import Session as sqla_Session


class DataRepository():
    def __init__(self, **kwargs):
        if 'session' in kwargs:
            if not isinstance(kwargs['session'], sqla_Session):
                raise AttributeError('session provided is not a SQLA-Session')
            self.session = kwargs['session']
        else:
            self.session = None
