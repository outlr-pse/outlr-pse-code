from io import BytesIO
from typing import Optional

import pandas as pd

from models.dataset import Dataset


def csv_to_dataset(name: str, dataset: str) -> Dataset:
    """Converts a CSV string to a Dataset object.
    Args:
        name: The name of the dataset.
        dataset: The path to the CSV file.
    Returns:
        Dataset: The Dataset object.

    """
    df = pd.read_csv(dataset)
    dataset = Dataset(name, df)

    return dataset


def csv_to_list(csv: str) -> list:
    """Converts a CSV file to a list.
    Args:
        csv: The path to the CSV file.
    Returns:
        list: The list of datapoints.
    """
    df = pd.read_csv(csv, header=None)

    return df[0].tolist()


def write_list_to_csv(data: list[int], path: Optional[str] = None) -> BytesIO | None:
    """Converts a list of integers to a CSV file.
    Args:
        path: The path to the CSV file.
        data: The list of datapoints.
    Returns:
        BytesIO: In-memory file-like object if `path` is not provided.
        None: If `path` is provided.
    """
    path_or_buf = path or BytesIO()
    pd.DataFrame([data]).to_csv(path_or_buf, index=False, header=False)
    if not path:
        path_or_buf.seek(0)
        return path_or_buf
