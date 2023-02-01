from models.subspacelogic.subspacelogic import *
import numpy as np
from numpy.typing import ArrayLike


class Literal(SubspaceLogic):
    """This class represents a literal in the subspace logic
    A literal is a leaf in the tree.
    This class is part of a composite pattern.
    This class contains some static attributes that should be readonly.

    Attributes:
        subspace: A single Subspace
    """

    JSON_KEY = "literal"
    SUBSPACE_JSON_KEY = "subspace"

    def __init__(self, subspace: Subspace):
        """Create a new Literal
        Args:
            subspace: A single Subspace
        """
        self.subspace = subspace

    def get_subspaces(self) -> set[Subspace]:
        return {self.subspace}

    def evaluate(self) -> ArrayLike:
        # create numpy array containing 0 and 1
        dataset_size = 10  # TODO set to self.subspace.experiment_result.experiment.dataset_size
        array = np.zeros(dataset_size, np.uint8)
        for outlier in self.subspace.outliers:
            array[outlier.index] = 1
        return array

    def to_json(self) -> dict:
        return {
            Literal.JSON_KEY: {
                Literal.SUBSPACE_JSON_KEY: self.subspace.to_json()
            }
        }

    @staticmethod
    def from_json(json: dict) -> 'Literal':
        return Literal(
            subspace=Subspace.from_json(json[Literal.SUBSPACE_JSON_KEY])
        )
