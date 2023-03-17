from typing import Any
from concurrent.futures import Executor
import concurrent.futures as futures

import pandas as pd
from numpy.typing import NDArray

from models.odm.odm import ODM
from execution.odm_scheduler import ODMScheduler


class ExecutorODMScheduler(ODMScheduler):
    """
    An ODMScheduler that is build around the ``concurrent.futures.Executor`` class.
    An ``Executor`` is used to run the outlier detection method
    """

    def __init__(self, executor: Executor):
        """
        Args:
            executor (concurrent.futures.Executor): A ``concurrent.futures.Executor`` that is used to execute the odm
        """
        self.executor = executor

    def schedule(self, odm: ODM, hyperparams: dict[str, Any],
                 dataset: pd.DataFrame) -> futures.Future[(NDArray, NDArray)]:
        return self.executor.submit(odm.run_odm, dataset, hyperparams)
