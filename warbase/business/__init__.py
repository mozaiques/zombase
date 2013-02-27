from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLA_Session

from warbase.model import User
from warbase.data import DataRepository


class AbcBusinessWorker(DataRepository):
    """ABC for business objects.

    Provide a base with a fully functionnal SQLA-Session.

    """
    pass
