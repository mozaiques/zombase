from warbmodel import User

from . import DataRepository


class UsersData(DataRepository):

    def create(self, **kwargs):
        # Validate datas
        user_schema = User.UserSchema(kwargs)

        user = User.User(**kwargs)
        self.session.add(user)

        # To get a full user to return (get a working id)
        self.session.flush()

        return user
