import unittest

from models.odm.odm import ODM
from odmprovider.pyod_scraper import PyODScraper


class MyTestCase(unittest.TestCase):

    def test_scraper(self):
        pyod_scraper = PyODScraper()
        odm = PyODScraper.next_odm(pyod_scraper)
        self.assertIsInstance(odm, ODM)
