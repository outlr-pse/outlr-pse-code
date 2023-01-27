from models.subspacelogic.subspace_logic import *


class Literal(SubspaceLogic):

    def __int__(self, subspace: Subspace):
        self.subspace = subspace

    def get_subspaces(self) -> list[Subspace]:
        return [self.subspace]

    def evaluate(self) -> list[int]:
        return list(map(lambda outlier: outlier.index, self.subspace.outliers))
