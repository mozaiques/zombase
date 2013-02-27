from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLA_Session


class AbcBusinessWorker():
    """ABC for business objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def __init__(self, **kwargs):
        """Init a "normal" SQLA-Session."""
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        if not isinstance(kwargs['session'], SQLA_Session):
            raise AttributeError('session provided is not a SQLA-Session')

        self.session = kwargs['session']
