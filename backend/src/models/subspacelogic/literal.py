from models.subspacelogic.subspacelogic import *
from numpy.typing import ArrayLike


class Literal(SubspaceLogic):
    """This class represents a literal in the subspace logic
    A literal is a leaf in the tree.
    This class is part of a composite pattern.

    Attributes:
        subspace: A single Subspace
    """

    def __int__(self, subspace: Subspace):
        """Create a new Literal
        Args:
            subspace: A single Subspace
        """
        self.subspace = subspace

    def get_subspaces(self) -> set[Subspace]:
        return {self.subspace}

    def evaluate(self) -> ArrayLike:
        return list(map(lambda outlier: outlier.index, self.subspace.outliers))
