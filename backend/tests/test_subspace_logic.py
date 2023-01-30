import unittest

from models.subspacelogic.literal import *
from models.subspacelogic.operation import *
from models.results.subspace_outlier import Subspace, Outlier


class TestSubspaceLogic(unittest.TestCase):

    outlier2 = Outlier(2)
    outlier3 = Outlier(3)
    subspace1 = Subspace(5, [1, 3, 6], [outlier3, outlier2])
    subspace2 = Subspace(4, [1, 4, 5], [Outlier(1), outlier3])
    subspace3 = Subspace(6, [0, 2, 23], [outlier2, outlier3, Outlier(99)])
    sub1: Literal = Literal(subspace1)
    sub2: Literal = Literal(subspace2)
    sub3: Literal = Literal(subspace3)

    level1: Operation(logical_or, [sub1, sub2])
    level2: Operation(logical_and, [level1, level1])
    level3: Operation(logical_or, [level1, level2, sub3])

    def test_level3_subspaces(self):
        subspaces: set[Subspace] = self.level3.get_subspaces()
        self.assertIn(self.subspace1, subspaces)
        self.assertIn(self.subspace3, subspaces)
        self.assertIn(self.subspace2, subspaces)
        self.assertEqual(len(subspaces), 3)
