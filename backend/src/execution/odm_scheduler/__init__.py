from typing import Any
from abc import ABC, abstractmethod
import concurrent.futures as futures

import pandas as pd
from numpy.typing import NDArray

from models.odm.odm import ODM


class ODMScheduler(ABC):
    """
    A scheduler that can scheduler the execution of individual outlier detection methods
    """

    @abstractmethod
    def schedule(self, odm: ODM, hyperparams: dict[str, Any],
                 dataset: pd.DataFrame) -> futures.Future[(NDArray, NDArray)]:
        """
        Schedule the execution of an individual outlier detection method
        Args:
            odm: ODM to be used
            hyperparams: Hyperparameters to be used
            dataset: The dataset to be used. This can be a dataset that is reduced to a subspace
        Returns: Returns a future containing the result of the outlier detection method.
            The result is a numpy array containing 0 and 1 for each datapoint indicating if the point is an outlier.
            The future will contain an exception if the execution raised and exception.
        """
        pass
