import numpy as np
import pandas as pd

from models.dataset.dataset import Dataset


def csv_to_dataset(name: str, dataset: str) -> Dataset:

    """Converts a CSV string to a Dataset object.
    Args:
        name (str): The name of the dataset.
        dataset (str): The path to the CSV file.
    Returns:
        Dataset: The Dataset object.

    """
    df = pd.read_csv(dataset)
    dataset = Dataset(name, df)

    return dataset

def csv_to_groundtruth(groundtruth: str) -> np.ndarray:
    """Converts a CSV string to a groundtruth array.
    Args:
        groundtruth (str): The path to the CSV file.
    Returns:
        np.ndarray: The groundtruth array.
    """
    df = pd.read_csv(groundtruth)

    return df.to_numpy(dtype=int)

def csv_to_groundtruth(name: str, groundtruth: str) -> np.ndarray:

    """Converts a CSV string to a Dataset object.
    Args:
        name (str): The name of the dataset.
        dataset (str): The path to the CSV file.
    Returns:
        Dataset: The Dataset object.

    """
    df = pd.read_csv(dataset)
    dataset = Dataset(name, df)

    return dataset
