import unittest
import pandas as pd
import numpy as np

from models.dataset.dataset import Dataset
from util.data import csv_to_dataset, csv_to_ndarray, ndarray_to_csv


class TestCsvMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a sample csv file
        cls.sample_csv = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        cls.sample_csv.to_csv("sample.csv", index=False)

        # create a sample numpy array
        cls.sample_array = np.array([[1, 2, 3], [4, 5, 6]])

        # test the ndarray_to_csv function
        ndarray_to_csv("sample_array.csv", cls.sample_array)
    @classmethod
    def tearDownClass(cls):
        # remove the sample csv file
        import os
        os.remove("sample.csv")
        os.remove("sample_array.csv")

    def test_csv_to_dataset(self):
        # test the csv_to_dataset function
        result = csv_to_dataset("sample", "sample.csv")
        expected = Dataset("sample", self.sample_csv)
        self.assertEqual(result.name, expected.name)
        self.assertTrue(result.dataset.equals(expected.dataset))

    def test_csv_to_ndarray(self):
        # test the csv_to_ndarray function
        result = csv_to_ndarray("sample.csv")
        expected = self.sample_csv.to_numpy(dtype=int)
        self.assertTrue(np.array_equal(result, expected))

    def test_ndarray_to_csv(self):
        result = pd.read_csv("sample_array.csv", header=None)
        expected = pd.DataFrame(self.sample_array)
        self.assertTrue(np.array_equal(result, expected))
