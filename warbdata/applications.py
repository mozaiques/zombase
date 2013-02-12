from warbmodel import Application

from . import DataRepository


class ApplicationsData(DataRepository):
    """DataRepository object for applications."""

    def create(self, **kwargs):
        """Create and insert an application in DB.

        Keyword arguments:
        see warbmodel.Application.ApplicationSchema

        """
        app_schema = Application.ApplicationSchema(kwargs)  # Validate datas

        app = Application.Application(**kwargs)
        self.session.add(app)

        # To get a full application to return (get a working id)
        self.session.flush()

        return app
