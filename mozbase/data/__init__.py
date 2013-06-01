from mozbase.model import User


class DataRepository():
    """ABC for data repository objects."""

    def __init__(self, dbsession=None, **kwargs):
        """Associate database session to Repository."""
        if not dbsession:
            raise TypeError('Databse session not provided')

        self._dbsession = dbsession

    def _get_user(self, user_id=None, user=None, **kwargs):
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


class AuthenticatedDataRepository(DataRepository):
    """ABC for data repository objects with user information."""

    def __init__(self, dbsession=None, user=None, user_id=None, **kwargs):
        """Associate database session and user to Repository."""
        DataRepository.__init__(self, dbsession)
        self._user = self._get_user(user_id, user)
