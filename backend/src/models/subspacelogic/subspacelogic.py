from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import *

import models.subspacelogic as subspacelogic
from models.json_error import JSONError
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
    def evaluate(self) -> ArrayLike:
        """
        Evaluates the subspace logic.
        It is required that all subspaces contained in this subspace logic have their result in the
        Subspace.outliers attribute. See SubspaceLogic.get_subspaces

        Returns:
            A numpy array where the element at index i is 1 if and only if the datapoint at index i in the dataset
            is considered an outlier using the subspace logic.
        """
        pass

    @abstractmethod
    def to_json(self) -> dict:
        """
        Converts to SubspaceLogic to a dictionary that represents a json.

        The resulting JSON is of the shape ``{logic_type: {...}}``, where ``logic_type`` determines the subclass.

        Returns:
            Returns the JSON representation in the form of a dict
        """
        pass

    @staticmethod
    def from_json(json: dict) -> 'SubspaceLogic':
        """
        Create a SubspaceLogic from JSON (in the form of a dict).

        A JSON must be of the shape ``{logic_type: {...}}``, where ``logic_type`` determines the subclass.
        The ``SubspaceLogic`` (base) class is responsible for checking ``logic_type`` and then calls ``from_json`` on the
        given subclass, where only the ``{...}`` part of the JSON above is passed.

        Raises:
            JSONError: Raises a ``JSONError`` when the given ``json`` cannot be parsed to a ``SubspaceLogic``
        """
        if len(json.keys()) != 1:
            raise JSONError("SubspaceLogic JSON contained other than a single key at the top level." +
                            "Every JSON must have the shape of the following example: {operation: {...}}")
        logic_type = next(iter(json.keys()))  # get the single key from the dict
        match logic_type:
            case subspacelogic.operation.Operation.JSON_KEY:
                return subspacelogic.operation.Operation.from_json(json[logic_type])
            case subspacelogic.literal.Literal.JSON_KEY:
                return subspacelogic.literal.Literal.from_json(json[logic_type])
            case _: raise JSONError(f"SubspaceLogic JSON contained an unknown type of subspace logic: {logic_type}")

