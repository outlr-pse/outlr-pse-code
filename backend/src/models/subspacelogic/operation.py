from itertools import chain
from numpy.typing import ArrayLike

from models.subspacelogic.operator import Operator
from models.subspacelogic.subspacelogic import *


class Operation(SubspaceLogic):
    """This class represents an operation in the subspace logic
    This class is part of a composite pattern.
    This class contains some class attributes that should be readonly

    Attributes:
        operator (Operator): Operator to be used
        operands (list[SubspaceLogic]): Contains the operands of the operation
    """

    JSON_TO_OPERATOR_MAP: dict[str, Operator] | None = None
    JSON_KEY = "operation"
    OPERATOR_JSON_KEY = "operator"
    OPERANDS_JSON_KEY = "operands"
    DATABASE_JSON_KEY = "o"
    DATABASE_OPERATOR_JSON_KEY = "f"
    DATABASE_OPERANDS_JSON_KEY = "a"

    def __init__(self, operator: Operator, operands: list[SubspaceLogic]):
        """Create a new Operation
        Args:
            operator (Operator): See attribute operator
            operands (list[SubspaceLogic]): See attribute operands
        """
        self.operator = operator
        self.operands = operands

    def get_subspaces(self) -> set[Subspace]:
        return set(chain(*map(lambda operand: operand.get_subspaces(), self.operands)))

    def evaluate(self, dataset_size: int) -> ArrayLike:
        return self.operator.function([operand.evaluate(dataset_size) for operand in self.operands])

    def to_client_json(self) -> dict:
        return {
            Operation.JSON_KEY: {
                Operation.OPERATOR_JSON_KEY: self.operator.json_name,
                Operation.OPERANDS_JSON_KEY: [operand.to_client_json() for operand in self.operands]
            }
        }

    @staticmethod
    def from_client_json(json: dict, existing_subspaces: dict[frozenset, Subspace]) -> 'Operation':
        return Operation(
            operator=Operation.json_to_operator(json[Operation.OPERATOR_JSON_KEY]),
            operands=list(map(
                lambda operand_json: SubspaceLogic.from_client_json(operand_json, existing_subspaces),
                json[Operation.OPERANDS_JSON_KEY])
            )
        )

    def to_database_json(self) -> dict:
        return {
            Operation.DATABASE_JSON_KEY: {
                Operation.DATABASE_OPERATOR_JSON_KEY: self.operator.json_name,
                Operation.DATABASE_OPERANDS_JSON_KEY: [operand.to_database_json() for operand in self.operands]
            }
        }

    @staticmethod
    def from_database_json(json: dict, subspaces: dict[int, Subspace]) -> 'Operation':
        return Operation(
            operator=Operation.json_to_operator(json[Operation.DATABASE_OPERATOR_JSON_KEY]),
            operands=list(map(
                lambda operand_json: SubspaceLogic.from_database_json(operand_json, subspaces),
                json[Operation.DATABASE_OPERANDS_JSON_KEY])
            )
        )

    @staticmethod
    def json_to_operator(operator_name: str) -> Operator:
        """
        Convert the JSON of an operator (which is just a str) to the actual Operator
        Args:
            operator_name: JSON of an operator (which is just a str)

        Returns:
            The actual Operator (which has .json_name == json)

        Raises:
            JSONError: Raises a JSONError when the operator is unknown
        """
        if Operation.JSON_TO_OPERATOR_MAP is None:  # lazily create dict from the Operator enum
            Operation.JSON_TO_OPERATOR_MAP = {enum_entry.json_name: enum_entry for enum_entry in Operator}
        if operator_name not in Operation.JSON_TO_OPERATOR_MAP.keys():
            raise JSONError(f"SubspaceLogic JSON contained an unknown operator: {operator_name}")
        return Operation.JSON_TO_OPERATOR_MAP[operator_name]
