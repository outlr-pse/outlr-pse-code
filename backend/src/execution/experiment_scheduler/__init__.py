from abc import ABC, abstractmethod
from concurrent.futures import Future

import pandas as pd
from sklearn import metrics

from execution.execution_error import ExecutionError
from execution.execution_error.subspace_error import SubspaceError
from execution.odm_scheduler import ODMScheduler
from models.experiment import Experiment, Subspace, Outlier, ExperimentResult
from models.subspacelogic import SubspaceLogic


class ExperimentScheduler(ABC):
    """
    A scheduler that can schedule the execution of an experiment.
    """

    def __init__(self, odm_scheduler: ODMScheduler):
        """
        Args:
            odm_scheduler: The ``ODMScheduler`` that is used to schedule the execution of individual ODMs
        """
        self.odm_scheduler = odm_scheduler

    @abstractmethod
    def schedule(self, experiment: Experiment) -> Future[None]:
        """
        Schedule the execution of an experiment.
        This method writes the result into the passed ``experiment``.
        This method expects the passed experiment to be not added to any session,
        that means it must be either transient or detached.
        Args:
            experiment: The experiment to be executed (in transient or detached state)
        Returns: Returns a future containing just None.
            The future can be used to add callbacks that are called once the execution is finished.
            The future is guaranteed to contain no exceptions.
        """
        pass

    @staticmethod
    def fail_execution(experiment: Experiment, error: ExecutionError):
        """
        Set the experiment to a "failed state".
        That means removing all results from the experiment, and it's child objects.
        More specifically the experiment_result and the outliers of all subspaces are removed.
        Also, an error_json is added to the experiment.
        This method should be called when the execution fails.
        Args:
            experiment: The experiment that failed
            error: The error that occurred during execution
        """
        experiment.error_json = error.to_json()
        experiment.experiment_result = None
        for subspace in experiment.subspaces:
            subspace.outliers = []

    @staticmethod
    def create_outlier_objects(experiment_result: ExperimentResult, subspaces: list[Subspace]) -> None:
        """
        Creates outlier objects that for all outliers in the experiment. Also includes the result_space
        This ensures that outliers that occur in multiple subspaces are only created once
        This uses the subspace.outlier_array attribute
        """
        outlier_map: dict[int, Outlier] = {}

        def get_or_create_outlier(index: int, result: ExperimentResult | None) -> Outlier:
            if index in outlier_map:
                return outlier_map[index]
            out = Outlier(index=index, experiment_result=result)
            outlier_map[index] = out
            return out

        def set_outliers_in_subspace(sub: Subspace, result: ExperimentResult | None):
            sub.outliers = []
            outlier_indices = (i for i, x in enumerate(sub.outlier_array) if x)
            for outlier_index in outlier_indices:
                outlier = get_or_create_outlier(outlier_index, result)
                sub.outliers.append(outlier)

        for subspace in subspaces:
            set_outliers_in_subspace(subspace, experiment_result)
        set_outliers_in_subspace(experiment_result.result_space, None)

    @staticmethod
    def write_result_space(experiment_result: ExperimentResult, subspace_logic: SubspaceLogic):
        """
        Calculates the result space (subspace with applied subspace logic)
        and adds it to the experiment
        """
        experiment_result.result_space = Subspace(name="result")
        experiment_result.result_space.outlier_array = subspace_logic.evaluate_labels()
        experiment_result.result_space.scores_array = subspace_logic.evaluate_scores()

    @staticmethod
    def write_metrics(experiment: Experiment):
        """
        Calculates the accuracy of the experiment and writes it to the experiment
        """
        ground_truth = experiment.ground_truth
        experiment_result = experiment.experiment_result
        outlier_array = experiment_result.result_space.outlier_array
        scores_array = experiment_result.result_space.scores_array

        if ground_truth is None:
            return

        experiment_result.accuracy = metrics.accuracy_score(ground_truth, outlier_array)

        if scores_array is None:
            return
        ground_truth = ground_truth[~pd.isna(scores_array)]
        scores_array = scores_array[~pd.isna(scores_array)]
        fpr, tpr, thresholds = metrics.roc_curve(ground_truth, scores_array)
        auc = metrics.auc(fpr, tpr)
        experiment_result.fpr = fpr.tolist()
        experiment_result.tpr = tpr.tolist()
        experiment_result.thresholds = thresholds.tolist()
        experiment_result.auc = auc

    @staticmethod
    def get_subspace(dataset: pd.DataFrame, columns: list[int]):
        """
        Get a subspace from a dataset
        Args:
            dataset: The dataset to get the subspace from
            columns: The columns of the subspace
        Returns:
            The subspace
        Raises:
            SubspaceError: If a column index of a subspace is out of bounds
        """
        try:
            return dataset.iloc[:, columns]
        except IndexError as e:
            raise SubspaceError() from e
