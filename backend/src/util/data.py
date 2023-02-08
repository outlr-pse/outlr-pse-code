import numpy as np
import pandas as pd
from typing import IO

from models.dataset.dataset import Dataset


def csv_to_dataset(name: str, dataset: "IO[bytes]") -> Dataset:
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


def csv_to_ndarray(csv: str) -> np.ndarray:
    """Converts a CSV file to a numpy ndarray.
    Args:
        csv (str): The path to the CSV file.
    Returns:
        np.ndarray: The numpy ndarray array.
    """
    df = pd.read_csv(csv)

    return df.to_numpy(dtype=int)


def ndarray_to_csv(path: str, arr: np.ndarray) -> None:
    """Converts numpy ndarray to a CSV file.
    Args:
        path (str): The path to the CSV file.
        arr (np.ndarray): The numpy ndarray array.
    Returns:
        None
    """
    pd.DataFrame(arr).to_csv(path, index=False, header=False)
