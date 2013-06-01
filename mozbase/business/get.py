from . import AbcBusinessWorker


class GetWorker(AbcBusinessWorker):

    def user(self, **kwargs):
        """Return a fully populated user given a user_id or a SQLA-User."""
        user = self._get_user(**kwargs)

        return user
