from data import user, action


class BusinessWorker():

    def __init__(self, **kwargs):
        self.user = user.UserData(**kwargs)
        self.action = action.ActionData(**kwargs)