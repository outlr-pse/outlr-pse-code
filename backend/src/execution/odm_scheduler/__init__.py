from typing import Any, Awaitable
from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
from numpy.typing import NDArray

from models.odm.odm import ODM
from execution.execution_error import ExecutionError


class ODMScheduler(ABC):
    """
    Represents a scheduler that can scheduler the execution of individual outlier detection methods
    """

    @abstractmethod
    def schedule(
        self,
        odm: ODM,
        hyperparams: dict[str, Any],
        dataset: pd.DataFrame
    ) -> Awaitable[NDArray]:
        """
        Schedule the execution of an individual outlier detection method
        Args:
            odm: ODM to be used
            hyperparams: Hyperparameters to be used
            dataset: The dataset to be used. This can be a dataset that is reduced to a subspace
        Raises: Raises an ExecutionError if the execution fails
        """
        pass
