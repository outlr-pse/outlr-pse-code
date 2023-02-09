from typing import TypeAlias, Callable
from enum import Enum
import numpy as np
from numpy.typing import ArrayLike

OperatorFn: TypeAlias = Callable[[list[ArrayLike]], ArrayLike]
"""OperatorFn type alias.
A function that defines the combination of some numpy integer arrays where each integer is either 1 or 0
into a single numpy integer array where each integer is either 1 or 0.
"""


def logical_and(arrays: list[ArrayLike]) -> ArrayLike:
    """Logical AND Operator function"""
    return np.logical_and.reduce(arrays)


def logical_or(arrays: list[ArrayLike]) -> ArrayLike:
    """Logical OR Operator function"""
    return np.logical_or.reduce(arrays)


class Operator(Enum):
    """Operator enum
    This enum represents an operator that is supported as a subspace

    Attributes
        LOGICAL_OR (Operator): A logical or operator
        LOGICAL_AND (Operator): A logical and operator
    """

    LOGICAL_OR = (logical_or, "or")
    LOGICAL_AND = (logical_and, "and")

    def __init__(self, function: OperatorFn, json_name: str):
        self.function = function
        self.json_name = json_name
