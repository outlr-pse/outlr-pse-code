import unittest

from models.odm.odm import ODM
from odmprovider.pyod_scraper import PyODScraper


class MyTestCase(unittest.TestCase):

    def test_scraper(self):
        pyod_scraper = PyODScraper()
        odm = pyod_scraper.get_odms()
        for o in odm:
            self.assertIsInstance(o, ODM)
