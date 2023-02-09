from typing import Any

import pandas as pd
from numpy.typing import NDArray

from models.odm.odm import ODM
from execution.odm_scheduler import ODMScheduler
from execution.execution_error.odm_failure_error import ODMFailureError


class SequentialODMScheduler(ODMScheduler):
    """
    A scheduler that runs the ODM sequentially.
    This is implemented using coroutines, but since the coroutine never awaits, the execution is sequential.
    """

    async def schedule(
        self,
        odm: ODM,
        hyperparams: dict[str, Any],
        dataset: pd.DataFrame
    ) -> NDArray:
        """
        Schedule the execution of an individual outlier detection method
        Args:
            odm: ODM to be used
            hyperparams: Hyperparameters to be used
            dataset: The dataset to be used. This can be a dataset that is reduced to a subspace
        Raises: ODMFailureError: Raises and ODMFailureError if the execution fails
        """
        try:
            result = odm.run_odm(dataset, hyperparams)
        except Exception as e:
            raise ODMFailureError(str(e))
        return result
