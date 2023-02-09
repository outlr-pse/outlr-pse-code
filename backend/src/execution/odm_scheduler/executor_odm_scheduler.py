from typing import Awaitable, Any
from concurrent.futures import Executor
import asyncio

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

    def schedule(self, odm: ODM, hyperparams: dict[str, Any], dataset: pd.DataFrame) -> Awaitable[NDArray]:
        return asyncio.wrap_future(
            self.executor.submit(odm.run_odm, dataset, hyperparams)
        )
