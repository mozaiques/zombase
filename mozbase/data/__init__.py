from mozbase.model import User


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    Handle cache interaction.

    """

    def __init__(self, **kwargs):
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        self.session = kwargs['session']

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
