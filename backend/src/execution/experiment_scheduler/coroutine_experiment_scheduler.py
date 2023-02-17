import asyncio
from datetime import datetime

from execution.experiment_scheduler import ExperimentScheduler
from execution.execution_error import ExecutionError
from models.experiment import Experiment, ExperimentResult


class CoroutineExperimentScheduler(ExperimentScheduler):
    """
    A scheduler that runs the experiment in a coroutine.
    This means that the execution happens more or less sequentially, but at some points in the execution the
    coroutine waits, which allows other coroutines to run.
    """

    async def schedule(self, experiment: Experiment) -> None:
        experiment.experiment_result = ExperimentResult(execution_date=datetime.now())
        try:
            subspace_results = await asyncio.gather(*[
                self.odm_scheduler.schedule(
                    experiment.odm,
                    experiment.param_values,
                    ExperimentScheduler.get_subspace(experiment.dataset.dataset, subspace.columns)
                ) for subspace in experiment.subspaces
            ])
            for index, result in enumerate(subspace_results):
                experiment.subspaces[index].outlier_array = result

            ExperimentScheduler.write_result_space(experiment.experiment_result, experiment.subspace_logic)
            ExperimentScheduler.create_outlier_objects(experiment.experiment_result, experiment.subspaces)
            ExperimentScheduler.write_accuracy(experiment.experiment_result, experiment.ground_truth)
            experiment.experiment_result.execution_time = datetime.now() - experiment.experiment_result.execution_date

        except ExecutionError as e:
            ExperimentScheduler.fail_execution(experiment, e)
        except Exception as e:
            ExperimentScheduler.fail_execution(experiment, ExecutionError(str(e)))
