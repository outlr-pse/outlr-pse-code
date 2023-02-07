from abc import ABC, abstractmethod
from numpy.typing import *

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.json_error import JSONError
from models.experiment import Subspace
from models.base import Base


class SubspaceLogic(ABC):
    """This interface represents the subspace logic.
    This class is part of a composite pattern.
    """

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


    @abstractmethod
    def get_subspaces(self) -> set['Subspace']:
        """
        Get subspaces
        Returns:
            Returns the set of subspaces that are contained in this subspace logic
        """
        pass

    @abstractmethod
    def evaluate(self, dataset_size: int) -> ArrayLike:
        """
        Evaluates the subspace logic.
        It is required that all subspaces contained in this subspace logic have their result in the
        Subspace.outliers attribute. See SubspaceLogic.get_subspaces

        Args:
            dataset_size (int): The size of the dataset. Needed to know size of arrays for calculation

        Returns:
            A numpy array where the element at index i is 1 if and only if the datapoint at index i in the dataset
            is considered an outlier using the subspace logic.
        """
        pass

    @abstractmethod
    def to_client_json(self) -> dict:
        """
        Convert SubspaceLogic to a dictionary that represents a json to be sent to a client.

        The resulting JSON is of the shape ``{logic_type: {...}}``, where ``logic_type`` determines the subclass.

        Returns:
            Returns the JSON representation in the form of a dict
        """
        pass

    @staticmethod
    def from_client_json(json: dict, existing_subspaces: dict[frozenset, 'Subspace']) -> 'SubspaceLogic':
        """
        Create a SubspaceLogic from JSON that was received from a client (in the form of a dict).

        A JSON must be of the shape ``{logic_type: {...}}``, where ``logic_type`` determines the subclass.
        The ``SubspaceLogic`` (base) class is responsible for checking ``logic_type``
        and then calls ``from_client_json`` on the
        given subclass, where only the ``{...}`` part of the JSON above is passed.

        Args:
            json (dict): JSON dict
            existing_subspaces (dict[int | frozenset, Subspace]):
                Dict that maps subspace columns to Subspace objects.
                Used so that subspaces that occur multiple times in the subspace logic are created only once

        Raises:
            JSONError: Raises a ``JSONError`` when the given ``json`` cannot be parsed to a ``SubspaceLogic``
        """
        if len(json.keys()) != 1:
            raise JSONError("SubspaceLogic JSON contained other than a single key at the top level." +
                            "Every JSON must have the shape of the following example: {operation: {...}}")
        logic_type = next(iter(json.keys()))  # get the single key from the dict
        match logic_type:
            case Operation.JSON_KEY:
                return Operation.from_client_json(json[logic_type], existing_subspaces)
            case Literal.JSON_KEY:
                return Literal.from_client_json(json[logic_type], existing_subspaces)
            case _: raise JSONError(
                f"SubspaceLogic JSON (client) contained an unknown type of subspace logic: {logic_type}"
            )

    def to_database_json(self) -> dict:
        """
        Convert SubspaceLogic to a JSON dict that can be stored in the database
        """
        pass

    @staticmethod
    def from_database_json(json: dict, subspaces: dict[int, 'Subspace']) -> 'SubspaceLogic':
        """
        Create a new SubspaceLogic from a json dict that was read from the database
        Args:
            json: JSON dict (from the database)
            subspaces: Maps subspace ids to Subspace objects.
            Must contain all Subspaces that occur in the subspace logic. Otherwise, an error is raised

        Raises:
            JSONError: Raises an Error if there is a subspace in the subspace logic
                that was not found in the ``subspace`` dict argument
            JSONError: Raises a ``JSONError`` when the given ``json`` cannot be parsed to a ``SubspaceLogic``
        """
        if len(json.keys()) != 1:
            raise JSONError("SubspaceLogic JSON contained other than a single key at the top level." +
                            "Every JSON must have the shape of the following example: {operation: {...}}")

        logic_type = next(iter(json.keys()))  # get the single key from the dict
        match logic_type:
            case Operation.DATABASE_JSON_KEY:
                return Operation.from_database_json(json[logic_type], subspaces)
            case Literal.DATABASE_JSON_KEY:
                return Literal.from_database_json(json[logic_type], subspaces)
            case _: raise JSONError(
                f"SubspaceLogic JSON (database) contained an unknown type of subspace logic: {logic_type}"
            )


from models.subspacelogic.literal import Literal
from models.subspacelogic.operation import Operation
