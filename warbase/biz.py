from business import get


class BusinessWorker():

    def __init__(self, **kwargs):
        self.get = get.GetWorker(**kwargs)