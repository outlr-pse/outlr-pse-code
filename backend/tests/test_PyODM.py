import unittest
import pyod
from models.odm.pyodm import PyODM


# TODO: Add more tests for Experiment, ODM and User
class TestPyODM(unittest.TestCase):
    def setUp(self):
        self.odm = PyODM(id=1, name='abod.ABOD', deprecated=False)

    def test_working(self):
        self.odm.run_odm(None, {'contamination': 0.1, 'n_neighbors': 5, 'method': 'fast'})
        #pyod.models.abod.ABOD({'contamination': 0.1, 'n_neighbors': 5, 'method': 'fast'})