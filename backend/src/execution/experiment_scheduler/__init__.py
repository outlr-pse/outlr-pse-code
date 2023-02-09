from abc import ABC, abstractmethod
from typing import Awaitable

import pandas as pd
import numpy as np
from numpy.typing import NDArray

from execution.execution_error import ExecutionError
from execution.odm_scheduler import ODMScheduler
from models.experiment import Experiment, Subspace, Outlier, ExperimentResult
from models.subspacelogic import SubspaceLogic


class ExperimentScheduler(ABC):
    """
    A scheduler that can schedule the execution of an experiment.
    """

    def __init__(self, odm_scheduler: ODMScheduler):
        self.odm_scheduler = odm_scheduler

    @abstractmethod
    def schedule(self, experiment: Experiment) -> Awaitable[None]:
        """
        Schedule the execution of an experiment
        This method writes the result into the passed ``experiment``
        This method is guaranteed to work even if the passed ``experiment`` is currently added to a database session
        Args:
            experiment: The experiment to be executed
        """
        pass

    @staticmethod
    def fail_execution(experiment: Experiment, error: ExecutionError):
        """
        Remove everything that relates to experiment results from an experiment.
        Add error to experiment
        This method should be called to reset experiments to a defined state when the execution fails
        Args:
            experiment: The experiment to reset
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
        experiment_result.result_space.outlier_array = subspace_logic.evaluate()

    @staticmethod
    def write_accuracy(experiment_result: ExperimentResult, ground_truth: NDArray):
        """
        Calculates the accuracy of the experiment and writes it to the experiment
        """

        correct_predictions = np.sum(ground_truth == experiment_result.result_space.outlier_array)
        experiment_result.accuracy = correct_predictions / ground_truth.size

    @staticmethod
    def get_subspace(dataset: pd.DataFrame, columns: list[int]):
        """
        Get a subspace from a dataset
        Args:
            dataset: The dataset to get the subspace from
            columns: The columns of the subspace

        Returns:
            The subspace
        """
        return dataset.iloc[:, columns]
