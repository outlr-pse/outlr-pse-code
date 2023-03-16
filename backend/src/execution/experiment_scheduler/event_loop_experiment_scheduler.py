import asyncio
from datetime import datetime
import concurrent.futures

from execution.experiment_scheduler import ExperimentScheduler
from execution.odm_scheduler import ODMScheduler
from execution.execution_error import ExecutionError
from models.experiment import Experiment, ExperimentResult


class EventLoopExperimentScheduler(ExperimentScheduler):
    """
    A scheduler that runs the experiment as a coroutine on a given event loop.
    The event loop can run on a different thread than the thread that calls the schedule method.
    """

    def __init__(self, odm_scheduler: ODMScheduler, loop: asyncio.AbstractEventLoop):
        """
        Args:
            odm_scheduler: The ``ODMScheduler`` that is used to schedule the execution of individual ODMs
            loop: The event loop on which the experiment execution is scheduled as a coroutine.
                The event loop is expected to be running.
                It can run on a different thread than the thread that calls ``__init__`` or ``schedule``.
        """
        super().__init__(odm_scheduler)
        self.loop = loop

    async def schedule_coroutine(self, experiment: Experiment) -> None:
        experiment.experiment_result = ExperimentResult(execution_date=datetime.now())
        try:
            subspace_results = await asyncio.gather(*[
                asyncio.wrap_future(
                    future=self.odm_scheduler.schedule(
                        experiment.odm,
                        experiment.param_values,
                        ExperimentScheduler.get_subspace(experiment.dataset, subspace.columns)
                    ),
                    loop=self.loop
                ) for subspace in experiment.subspaces
            ])
            for index, result in enumerate(subspace_results):
                labels, scores = result
                experiment.subspaces[index].outlier_array = labels
                experiment.subspaces[index].score_array = scores

            ExperimentScheduler.write_result_space(experiment.experiment_result, experiment.subspace_logic)
            ExperimentScheduler.create_outlier_objects(experiment.experiment_result, experiment.subspaces)
            ExperimentScheduler.write_metrics(experiment)
            experiment.experiment_result.execution_time = datetime.now() - experiment.experiment_result.execution_date

        except ExecutionError as e:
            ExperimentScheduler.fail_execution(experiment, e)
        except Exception as e:
            ExperimentScheduler.fail_execution(experiment, ExecutionError(type(e).__name__ + ": " + str(e)))

    def schedule(self, experiment: Experiment) -> concurrent.futures.Future[None]:
        # Schedule the coroutine in the given loop (which might be on another thread)
        return asyncio.run_coroutine_threadsafe(
            self.schedule_coroutine(experiment),
            self.loop
        )

    def stop(self) -> None:
        """
        Stop the event loop. The loop will not stop immediately.
        """
        self.loop.call_soon_threadsafe(self.loop.stop)
