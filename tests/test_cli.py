# -*- coding: utf-8 -*-
import unittest

from zombase import cli


class TestCLI(unittest.TestCase):

    def test_semver_without_dev(self):
        version = '1.2.3'

        release_version, next_dev_version = cli.compute_semver(version)

        self.assertEqual(release_version, '1.3.0')
        self.assertEqual(next_dev_version, '1.3.1dev')

        release_version, next_dev_version = cli.compute_semver(
            version, release='minor')

        self.assertEqual(release_version, '1.2.4')
        self.assertEqual(next_dev_version, '1.2.5dev')

        release_version, next_dev_version = cli.compute_semver(
            version, release='major')

        self.assertEqual(release_version, '2.0.0')
        self.assertEqual(next_dev_version, '2.0.1dev')

    def test_semver_with_dev(self):
        version = '1.2.3dev'

        release_version, next_dev_version = cli.compute_semver(version)

        self.assertEqual(release_version, '1.3.0')
        self.assertEqual(next_dev_version, '1.3.1dev')

        release_version, next_dev_version = cli.compute_semver(
            version, release='minor')

        self.assertEqual(release_version, '1.2.3')
        self.assertEqual(next_dev_version, '1.2.4dev')

        release_version, next_dev_version = cli.compute_semver(
            version, release='major')

        self.assertEqual(release_version, '2.0.0')
        self.assertEqual(next_dev_version, '2.0.1dev')
