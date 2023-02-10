from typing import Callable
from threading import Thread

from numpy.typing import NDArray
import asyncio
from datetime import datetime, timedelta

from execution.experiment_scheduler import ExperimentScheduler
from execution.execution_error import ExecutionError
from models.experiment import Experiment, ExperimentResult, Subspace
import database.database_access as db


class CoroutineExperimentScheduler(ExperimentScheduler):
    """
    A scheduler that runs the experiment in a coroutine.
    This means that the execution happens more or less sequentially, but at some points in the execution
    coroutine waits, which allows other coroutines (for example api calls) to run.
    """

    async def schedule(self, experiment: Experiment) -> None:
        experiment_result = ExperimentResult(execution_date=datetime.now())
        subspaces = experiment.subspaces
        experiment.subspaces = []  # Make sure a session flush doesn't add partially initialized outliers to the db
        try:
            subspace_results = await asyncio.gather(*[
                self.odm_scheduler.schedule(
                    experiment.odm,
                    experiment.param_values,
                    ExperimentScheduler.get_subspace(experiment.dataset.dataset, subspace.columns)
                ) for subspace in subspaces
            ])
            for index, result in enumerate(subspace_results):
                subspaces[index].outlier_array = result

            ExperimentScheduler.write_result_space(experiment_result, experiment.subspace_logic)
            with db.session.no_autoflush:
                # The creation of outliers (which are added to subspaces) must be done without flushing the session
                ExperimentScheduler.create_outlier_objects(experiment_result, subspaces)
            ExperimentScheduler.write_accuracy(experiment_result, experiment.ground_truth)

            experiment_result.execution_time = datetime.now() - experiment_result.execution_date

            experiment.experiment_result = experiment_result
        except ExecutionError as e:
            ExperimentScheduler.fail_execution(experiment, e)
        # except Exception as e:
            # ExperimentScheduler.fail_execution(experiment, ExecutionError(str(e)))
        finally:
            experiment.subspaces = subspaces
