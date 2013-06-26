# -*- coding: utf-8 -*-
import unittest

import mozbase.data.fake__init__

from . import TestData


class DataRepository(TestData):

    def test_instancing_data_repo(self):
        mozbase.data.fake__init__.DataRepository(dbsession=self.session)

    def test_instancing_data_repo_without_session(self):
        with self.assertRaises(TypeError):
            mozbase.data.fake__init__.DataRepository()


if __name__ == '__main__':
    unittest.main()
