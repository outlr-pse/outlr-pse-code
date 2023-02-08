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


def csv_to_list(csv: str) -> list:
    """Converts a CSV file to a numpy ndarray.
    Args:
        csv (str): The path to the CSV file.
    Returns:
        np.ndarray: The numpy ndarray array.
    """
    df = pd.read_csv(csv, header=None)

    return df.values.tolist()[0]


def list_to_csv(path: str, data: list[int]) -> None:
    """Converts numpy ndarray to a CSV file.
    Args:
        path (str): The path to the CSV file.
        data (np.ndarray): The numpy ndarray array.
    Returns:
        None
    """
    pd.DataFrame([data]).to_csv(path, index=False, header=False)
