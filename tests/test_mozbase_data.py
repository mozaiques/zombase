 # -*- coding: utf-8 -*-
import unittest

import mozbase.data

from . import TestData


class DataRepository(TestData):

    def test_instancing_data_repo(self):
        mozbase.data.DataRepository(dbsession=self.session)

    def test_instancing_data_repo_without_session(self):
        with self.assertRaises(TypeError):
            mozbase.data.DataRepository()


if __name__ == '__main__':
    unittest.main()
