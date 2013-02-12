from sqlalchemy.orm.session import Session as SQLA_Session


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
