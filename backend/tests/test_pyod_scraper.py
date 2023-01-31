import unittest

from models.odm.odm import ODM
from odmprovider.pyod_scraper import PyODScraper


class MyTestCase(unittest.TestCase):

    def test_scraper(self):
        pyod_scraper = PyODScraper()
        odm = pyod_scraper.next_odm()
        self.assertEqual(next(odm), "abod")
        self.assertEqual(next(odm), "alad")
        for i in range(0, 10):
            next(odm)
        self.assertEqual(next(odm), "deep_svdd")

        odm = pyod_scraper.next_odm()
        for o in odm:
            self.assertIsInstance(o, ODM)

