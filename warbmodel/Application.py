from sqlalchemy import Column, Integer, String
from voluptuous import Schema, Required, All, Length, Url

from . import Base


class Application(Base):
    __tablename__ = 'wb_applications'
    id = Column(Integer, primary_key=True)

    # Internal use only
    name = Column(String(length=30), unique=True)
    url = Column(String(length=100), unique=True)
    min_permission = Column(String(length=10))

    # To display
    title = Column(String(length=30))
    picto = Column(String(length=30))  # HTML tag like <i class="icon-xxx"></i>


ApplicationSchema = Schema({
    Required('name'): All(str, Length(min=3, max=30)),
    Required('url'): All(str, Length(max=100), Url),
    Required('min_permission'): All(str, Length(min=1, max=10)),
    Required('title'): All(str, Length(min=1, max=30)),
    'picto': All(str, Length(max=30)),
})
