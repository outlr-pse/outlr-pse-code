from io import BytesIO
from typing import Optional

import pandas as pd
from matplotlib import pyplot as plt

from models.dataset import Dataset

from pyod.utils import generate_data


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

    return df.values.tolist()[0]


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


def generate_data_as_csv(contamination: float, n_samples: int, n_features: int,
                             path_dataset: str, path_groundtruth: str) -> None:
    """Generates a dataset and a groundtruth file.
    Args:
        contamination: The percentage of outliers.
        n_samples: The number of samples.
        n_features: The number of features.
        path_dataset: The path to the dataset file.
        path_groundtruth: The path to the groundtruth file.
    """
    n_train = n_samples  # number of training points
    X_train, y_train = generate_data(n_train=n_train, n_features=n_features,
                                                     contamination=contamination, train_only=True)
    X_train = pd.DataFrame(X_train)
    X_train.to_csv(path_dataset, index=False, header=False)
    y_train = pd.DataFrame(y_train)
    y_train.to_csv(path_groundtruth, index=False, header=False)

# def visualize_data(dataset: str, groundtruth: str) -> None:
#     """Visualizes a dataset and a groundtruth file.
#     Args:
#         dataset: The path to the dataset file.
#         groundtruth: The path to the groundtruth file.
#     """
#     df = pd.read_csv(dataset, header=None)
#     df = df.values.tolist()
#     df = pd.DataFrame(df, columns=["x", "y"])
#     df.plot.scatter(x="x", y="y", color='blue')
#     plt.show()
#     df = pd.read_csv(groundtruth, header=None)
#     df = df.values.tolist()
#     df = pd.DataFrame(df, columns=["x", "y"])
#     df.plot.scatter(x="x", y="y", color='red')
#     plt.show()

def visualize_data(path_dataset: str, path_groundtruth: str) -> None:
    X = pd.read_csv(path_dataset, header=None)
    y = pd.read_csv(path_groundtruth, header=None)

    inliers = X[y[0] == 0]
    outliers = X[y[0] == 1]

    plt.scatter(inliers[0], inliers[1], color='blue', label='Inliers')
    plt.scatter(outliers[0], outliers[1], color='red', label='Outliers')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    dataset: str = "C:\\Users\\erikw\\Downloads\\dataset.csv"
    groundtruth: str = "C:\\Users\\erikw\\Downloads\\groundtruth.csv"
    generate_data_as_csv(0.1, 200, 2, dataset, groundtruth)
    visualize_data(dataset, groundtruth)
