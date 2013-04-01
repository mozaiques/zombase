 # -*- coding: utf-8 -*-
import unittest

import warbase.data

from . import TestData


class DataRepository(TestData):

    def test_instancing_data_repo(self):
        warbase.data.DataRepository(session=self.session)

    def test_instancing_data_repo_without_session(self):
        with self.assertRaises(TypeError):
            warbase.data.DataRepository()


if __name__ == '__main__':
    unittest.main()
