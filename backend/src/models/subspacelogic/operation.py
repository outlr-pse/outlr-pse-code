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

    def __init__(self, operator: Operator, operands: list[SubspaceLogic]):
        """Create a new Operation
        Args:
            operator (Operator): See attribute operator
            operands (list[SubspaceLogic]): See attribute operands
        """
        self.operator = operator
        self.operands = operands

    def get_subspaces(self) -> set[Subspace]:
        return set(chain(map(lambda operand: operand.get_subspaces(), self.operands)))

    def evaluate(self) -> ArrayLike:
        return self.operator.function(list(map(lambda logic: logic.evaluate(), self.operands)))

    def to_json(self) -> dict:
        return {
            Operation.JSON_KEY: {
                Operation.OPERATOR_JSON_KEY: self.operator.json_name,
                Operation.OPERANDS_JSON_KEY: list(map(lambda operand: operand.to_json(), self.operands))
            }
        }

    @staticmethod
    def from_json(json: dict) -> 'Operation':
        return Operation(
            operator=json[Operation.OPERATOR_JSON_KEY],
            operands=list(map(
                lambda operand_json: SubspaceLogic.from_json(operand_json),
                json[Operation.OPERANDS_JSON_KEY])
            )
        )

    @staticmethod
    def json_to_operator(json: str) -> Operator:
        """
        Convert the JSON of an operator (which is just a str) to the actual Operator
        Args:
            json: JSON of an operator (which is just a str)

        Returns:
            The actual Operator (which has .json_name == json)

        Raises:
            JSONError: Raises a JSONError when the operator is unknown
        """
        if Operation.JSON_TO_OPERATOR_MAP is None:  # lazily create dict from the Operator enum
            Operation.JSON_TO_OPERATOR_MAP = {enum_entry.value.json_name: enum_entry.value for enum_entry in Operator}

        if json not in Operation.JSON_TO_OPERATOR_MAP.keys():
            raise JSONError(f"SubspaceLogic JSON contained an unknown operator: {json}")
        return Operation.JSON_TO_OPERATOR_MAP[json]
