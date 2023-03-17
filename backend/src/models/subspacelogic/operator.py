from typing import TypeAlias, Callable
from enum import Enum
import numpy as np
from numpy.typing import NDArray

OperatorFn: TypeAlias = Callable[[list[NDArray]], NDArray]
"""OperatorFn type alias.
A function that defines the combination of some numpy integer arrays where each integer is either 1 or 0
into a single numpy integer array where each integer is either 1 or 0.
"""


def logical_and_labels(arrays: list[NDArray]) -> NDArray:
    """Logical AND Operator function on the labels"""
    return np.logical_and.reduce(arrays)


def logical_and_scores(arrays: list[NDArray]) -> NDArray:
    """Logical AND Operator function on the scores"""
    return np.minimum.reduce(arrays)


def logical_or_labels(arrays: list[NDArray]) -> NDArray:
    """Logical OR Operator function on the labels"""
    return np.logical_or.reduce(arrays)


def logical_or_scores(arrays: list[NDArray]) -> NDArray:
    """Logical OR Operator function on the scores"""
    return np.maximum.reduce(arrays)


class Operator(Enum):
    """Operator enum
    This enum represents an operator that is supported as a subspace

    Attributes
        LOGICAL_OR (Operator): A logical or operator
        LOGICAL_AND (Operator): A logical and operator
    """

    LOGICAL_OR = (logical_or_labels, logical_or_scores, "or")
    LOGICAL_AND = (logical_and_labels, logical_or_scores, "and")

    def __init__(self, function_labels: OperatorFn, function_scores: OperatorFn, json_name: str):
        self.function_labels = function_labels
        self.function_scores = function_scores
        self.json_name = json_name
