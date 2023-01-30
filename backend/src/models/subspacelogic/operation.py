from typing import Callable, TypeAlias
from itertools import chain
import numpy as np
from numpy.typing import ArrayLike

from models.subspacelogic.subspacelogic import *


Operator: TypeAlias = Callable[[list[ArrayLike]], ArrayLike]
"""Operator type alias.
A function that defines the combination of numpy integer arrays where each integer is either 1 or 0.
"""


def logical_and(arrays: list[ArrayLike]) -> ArrayLike:
    """Logical AND Operator"""
    return np.logical_and.reduce(arrays)


def logical_or(arrays: list[ArrayLike]) -> ArrayLike:
    """Logical OR Operator"""
    return np.logical_or.reduce(arrays)


class Operation(SubspaceLogic):
    """This class represents an operation in the subspace logic
    This class is part of a composite pattern.

    Attributes:
        operator: A function that defines the combination of integer lists where each integer is either 1 or 0.
            An easy example would be a logical operation that acts point wise on its inputs.
        operands: Contains the operands of the operation
    """

    def __int__(self, operator: Operator, operands: list[SubspaceLogic]):
        """Create a new Operation
        Args:
            operator: See attribute operator
            operands: See attribute operands
        """
        self.operator = operator
        self.operands = operands

    def get_subspaces(self) -> set[Subspace]:
        return set(chain(map(lambda operand: operand.get_subspaces(), self.operands)))

    def evaluate(self) -> ArrayLike:
        return self.operator(list(map(lambda logic: logic.evaluate(), self.operands)))
