import unittest
import config


class TestConfig(unittest.TestCase):
    def test_config(self):
        self.assertIsNotNone(config.jwt_secret)
        self.assertIsNotNone(config.db_url)
