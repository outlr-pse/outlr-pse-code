from io import BytesIO
from typing import Optional
from pyod.models.knn import KNN   # kNN detector
import pandas as pd
from numpy.typing import NDArray
from matplotlib import pyplot as plt

from pyod.utils import generate_data


def csv_to_dataset(dataset: str) -> pd.DataFrame:
    """Converts a CSV string to a Dataset object.
    Args:
        dataset: The path to the CSV file.
    Returns:
        Dataset: The Dataset object.

    """
    return pd.read_csv(dataset, header=None)


def csv_to_numpy_array(csv: str) -> NDArray:
    """Converts a CSV file to a list.
    Args:
        csv: The path to the CSV file.
    Returns:
        list: The list of datapoints.
    """
    df = pd.read_csv(csv, header=None)

    return df[0].to_numpy()


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
    x_train, y_train = generate_data(n_train=n_train, n_features=n_features,
                                     contamination=contamination, train_only=True)
    x_train = pd.DataFrame(x_train)
    x_train.to_csv(path_dataset, index=False, header=False)
    y_train = pd.DataFrame(y_train)
    y_train.to_csv(path_groundtruth, index=False, header=False)


def visualize_data(path_dataset: str, path_groundtruth: str) -> None:
    x = pd.read_csv(path_dataset, header=None)
    y = pd.read_csv(path_groundtruth, header=None)

    inliers = x[y[0] == 0]
    outliers = x[y[0] == 1]

    plt.scatter(inliers[0], inliers[1], color='blue', label='Inliers')
    plt.scatter(outliers[0], outliers[1], color='red', label='Outliers')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    dataset: str = "C:\\Users\\erikw\\Downloads\\dataset2.csv"
    groundtruth: str = "C:\\Users\\erikw\\Downloads\\groundtruth2.csv"
    generate_data_as_csv(0.1, 20, 2, dataset, groundtruth)
    visualize_data(dataset, groundtruth)
