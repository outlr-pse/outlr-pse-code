import unittest
import pandas as pd

from models.dataset import Dataset
from util.data import csv_to_dataset, csv_to_numpy_array, write_list_to_csv


class TestCsvMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a sample csv file
        cls.sample_csv = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        cls.sample_csv.to_csv("sample.csv", index=False)

        # create a sample numpy array
        cls.sample_list = [1, 2, 3, 4, 5, 6]

    @classmethod
    def tearDownClass(cls):
        # remove the sample csv file
        import os
        os.remove("sample.csv")

    def test_csv_to_dataset(self):
        # test the csv_to_dataset function
        result = csv_to_dataset("sample", "sample.csv")
        expected = Dataset("sample", self.sample_csv)
        self.assertEqual(result.name, expected.name)
        self.assertTrue(result.dataset.equals(expected.dataset))

    @unittest.skip("Not implemented yet")
    def test_csv_to_list(self):
        # test the csv_to_ndarray function
        result = csv_to_numpy_array("sample.csv")
        expected = self.sample_csv.values.tolist()
        self.assertEqual(result, expected)

    @unittest.skip("Not implemented yet")
    def test_list_to_csv(self):
        # test the ndarray_to_csv function
        write_list_to_csv("sample_array.csv", self.sample_list)
        result = csv_to_numpy_array("sample_array.csv")
        self.assertEqual(result, self.sample_list)
