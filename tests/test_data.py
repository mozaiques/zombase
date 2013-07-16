# -*- coding: utf-8 -*-
import mozbase.data.fake__init__

from . import TestData


class TestDataRepository(TestData):

    def test_instancing_data_repo(self):
        class Bli():
            _dbsession = self.session

        mozbase.data.fake__init__.DataRepository(Bli())

    def test_instancing_data_repo_without_session(self):
        with self.assertRaises(TypeError):
            mozbase.data.fake__init__.DataRepository()

class InnerBoDataRepository(TestData):

    def test_instancing_inner_bo_data_repo(self):
        pass
