# -*- coding: utf-8 -*-
import unittest
import uuid

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dogpile.cache import make_region
from voluptuous import Schema

from zombase import database, foreman, worker


Base = declarative_base(cls=database.MetaBase)


class Mapping(Base):
    __tablename__ = 'mappings'
    id = Column(Integer, primary_key=True)


class MappingUUID(Base):
    __tablename__ = 'mappings_uuid'
    uuid = Column(database.GUIDType, primary_key=True, default=uuid.uuid4)


schema = Schema({
    'mapping': Mapping,
})

schema_uuid = Schema({
    'mapping': MappingUUID,
})


class TestWorkerResolveID(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        dbsession = Session()
        cache = make_region().configure('dogpile.cache.memory')
        setattr(dbsession, 'cache', cache)
        a_foreman = foreman.RawForeman(dbsession=dbsession)
        self.worker = worker.ObjectManagingWorker(
            a_foreman, managed_object=Mapping, managed_object_name='mapping')

    def tearDown(self):
        del self.worker

    def test_simple_resolve_id(self):
        mapping = Mapping(id=12)
        self.worker._dbsession.add(mapping)
        self.worker._dbsession.commit()

        a_dict = {'mapping_id': 12}
        a_dict = self.worker._resolve_id(a_dict, schema=schema)

        self.assertFalse('mapping_id' in a_dict)
        self.assertTrue('mapping' in a_dict)

    def test_simple_resolve_uuid(self):
        an_uuid = uuid.uuid4()
        mapping = MappingUUID(uuid=an_uuid)
        self.worker._dbsession.add(mapping)
        self.worker._dbsession.commit()

        a_dict = {'mapping_uuid': an_uuid}
        a_dict = self.worker._resolve_id(a_dict, schema=schema_uuid)

        self.assertFalse('mapping_uuid' in a_dict)
        self.assertTrue('mapping' in a_dict)

    def test_resolve_id_with_none(self):
        a_dict = {'mapping_id': None}
        a_dict = self.worker._resolve_id(
            a_dict, schema=schema, allow_none_id=True)

        self.assertEqual(a_dict['mapping'], None)

        a_second_dict = {'mapping_id': ''}
        a_second_dict = self.worker._resolve_id(
            a_second_dict, schema=schema, allow_none_id=True)

        self.assertEqual(a_second_dict['mapping'], None)
