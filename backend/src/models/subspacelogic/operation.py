from typing import Callable
from functools import *
from itertools import chain

from models.subspacelogic.subspace_logic import *


class Operation(SubspaceLogic):
    

    def __int__(self, operator: Callable[[list[list[int]]], list[int]], operands: list[SubspaceLogic]):
        self.operator = operator
        self.operands = operands

    def get_subspaces(self) -> list[Subspace]:
        return list(chain(map(lambda operand: operand.get_subspaces(), self.operands)))

    def evaluate(self) -> list[int]:
        return self.operator(list(map(lambda logic: logic.evaluate(), self.operands)))
