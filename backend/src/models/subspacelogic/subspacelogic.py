from abc import ABC, abstractmethod
import numpy as np

from models.results.subspace_outlier import Subspace


class SubspaceLogic(ABC):
    """This interface represents the subspace logic.
    This class is part of a composite pattern.
    """

    @abstractmethod
    def get_subspaces(self) -> set[Subspace]:
        """
        Get subspaces
        Returns:
            Returns the set of subspaces that are contained in this subspace logic
        """
        pass

    @abstractmethod
    def evaluate(self) -> np.typing.ArrayLike[int]:
        """
        Evaluates the subspace logic.
        It is required that all subspaces contained in this subspace logic have their result in the
        Subspace.outliers attribute. See SubspaceLogic.get_subspaces

        Returns:
            A numpy array where the element at index i is 1 if and only if the datapoint at index i in the dataset
            is considered an outlier using the subspace logic.
        """
        pass
