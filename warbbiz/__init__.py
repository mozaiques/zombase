from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLA_Session


class BusinessWorker():
    """ABC for business objects.

    Provide a base with two SQLA-Session (a fully functionnal and a read-only).

    """

    def __init__(self, **kwargs):
        """Init a "normal" and a read-only SQLA-Session."""
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        if not isinstance(kwargs['session'], SQLA_Session):
            raise AttributeError('session provided is not a SQLA-Session')

        self.session = kwargs['session']
        self.ro_session = self._create_ro_session(self.session)

    def _create_ro_session(self, session):
        """Return a read-only session built from a "normal" SQLA-Session."""
        roSession = sessionmaker(
            bind=session.bind,
            autoflush=False,
            autocommit=False)
        ro_session = roSession()

        # Monkey patching flush method
        ro_session.flush = self._abort_flush_ro

        return ro_session

    def _abort_flush_ro(*args, **kwargs):
        """Raise an exception if called."""
        raise IOError('Read-only Session trying to flush')
