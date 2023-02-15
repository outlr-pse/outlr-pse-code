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
        with db.session.no_autoflush:
            # Prevent session from flushing before the experiment is finished
            # TODO The session could still be flushed when other api requests are made, find a better solution
            experiment.subspaces = []
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
                ExperimentScheduler.create_outlier_objects(experiment_result, subspaces)
                ExperimentScheduler.write_accuracy(experiment_result, experiment.ground_truth)
                experiment_result.execution_time = datetime.now() - experiment_result.execution_date
                experiment.experiment_result = experiment_result

            except ExecutionError as e:
                CoroutineExperimentScheduler.clean_up_db(experiment_result, subspaces)
                ExperimentScheduler.fail_execution(experiment, e)
            except Exception as e:
                CoroutineExperimentScheduler.clean_up_db(experiment_result, subspaces)
                ExperimentScheduler.fail_execution(experiment, ExecutionError(str(e)))
            finally:
                experiment.subspaces = subspaces

    @staticmethod
    def clean_up_db(experiment_result: ExperimentResult, subspaces: list[Subspace]) -> None:
        """
        Removes the outlier objects from the database
        This is necessary because the outlier objects are not added to the session
        """
        with db.session.no_autoflush:
            for subspace in subspaces:
                subspace.experiment_result = None

        db.session.delete(experiment_result)
