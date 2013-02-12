from sqlalchemy import Column, Integer, String

from . import Base


class Application(Base):
    __tablename__ = "wb_applications"
    id = Column(Integer, primary_key=True)

    # Internal use only
    name = Column(String(length=30), unique=True)
    url = Column(String(length=100), unique=True)
    min_permission = Column(String(length=10))

    # To display
    title = Column(String(length=30))
    picto = Column(String(length=30))  # HTML tag like <i class="icon-xxx"></i>
