from typing import Any
import concurrent.futures as futures

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

    def schedule(self, odm: ODM, hyperparams: dict[str, Any], dataset: pd.DataFrame) -> futures.Future[NDArray]:
        # Run the outlier detection method sequentially and wrap its result in a future
        future = futures.Future()
        try:
            result = odm.run_odm(dataset, hyperparams)
            future.set_result(result)
        except Exception as e:
            future.set_exception(ODMFailureError(str(e)))
        return future
