from mozbase.model import User


class RawDataRepository():
    """Deepest object, only provide a database session."""

    def __init__(self, dbsession=None):
        """Associate database session."""
        if not dbsession:
            raise TypeError('Database session not provided')
        self._dbsession = dbsession


class DataRepository(RawDataRepository):
    """ABC for data repository objects."""

    def __init__(self, dbsession=None, **kwargs):
        RawDataRepository.__init__(self, dbsession)
        self._get = GetWorker(dbsession=dbsession)


class AuthenticatedDataRepository(DataRepository):
    """ABC for data repository objects with user informations."""

    def __init__(self, dbsession=None, user=None, user_id=None, **kwargs):
        """Associate database session and user to Repository."""
        DataRepository.__init__(self, dbsession)
        self._user = self._get.user(user_id, user)

class GetWorker(RawDataRepository):
    """Internal object to perform 'raw' gets."""

    def user(self, user_id=None, user=None, **kwargs):
        """Return a user given a user (other SQLA-Session) or a user_id."""
        if user:
            if not isinstance(user, User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            return self._dbsession.merge(user)

        elif user_id:
            return self._dbsession.query(User.User)\
                .filter(User.User.id == user_id)\
                .one()

        else:
            raise TypeError('User informations (user or user_id) not provided')