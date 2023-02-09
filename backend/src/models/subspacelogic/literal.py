import numpy as np
from numpy.typing import ArrayLike

from models.json_error import JSONError
from models.subspacelogic import SubspaceLogic, Subspace


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
    DATABASE_JSON_KEY = "l"
    DATABASE_SUBSPACE_JSON_KEY = "s"

    def __init__(self, subspace: Subspace):
        """Create a new Literal
        Args:
            subspace: A single Subspace
        """
        self.subspace = subspace

    def get_subspaces(self) -> set[Subspace]:
        return {self.subspace}

    def evaluate(self) -> ArrayLike:
        return self.subspace.outlier_array

    def to_client_json(self) -> dict:
        return {
            Literal.JSON_KEY: {
                Literal.SUBSPACE_JSON_KEY: self.subspace.to_json()
            }
        }

    @staticmethod
    def from_client_json(json: dict, existing_subspaces: dict[frozenset, Subspace]) -> 'Literal':
        subspace_cols: frozenset[int] = frozenset(json[Literal.SUBSPACE_JSON_KEY]["columns"])
        assert type(subspace_cols) is frozenset
        if subspace_cols in existing_subspaces:
            return Literal(subspace=existing_subspaces[subspace_cols])

        subspace = Subspace.from_client_json(json[Literal.SUBSPACE_JSON_KEY])
        existing_subspaces[subspace_cols] = subspace
        return Literal(subspace=subspace)

    def to_database_json(self) -> dict:
        return {
            Literal.DATABASE_JSON_KEY: {
                Literal.DATABASE_SUBSPACE_JSON_KEY: self.subspace.id
            }
        }

    @staticmethod
    def from_database_json(json: dict, subspaces: dict[int, Subspace]) -> 'Literal':
        subspace_id = json[Literal.DATABASE_SUBSPACE_JSON_KEY]
        if subspace_id not in subspaces:
            raise JSONError("Tried to read subspace logic JSON (from database) that contained "
                            "a subspace id which was not in the passes subspaces dict")
        return Literal(subspace=subspaces[subspace_id])
