from abc import ABC, abstractmethod

from models.results.subspace_outlier import Subspace


class SubspaceLogic(ABC):

    @abstractmethod
    def get_subspaces(self) -> list[Subspace]:
        pass

    @abstractmethod
    def evaluate(self) -> list[int]:
        pass
