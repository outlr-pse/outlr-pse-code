import unittest

from models.subspacelogic.literal import *
from models.subspacelogic.operation import *
from models.results.subspace_outlier import Subspace, Outlier


# don't modify these variables
outlier2 = Outlier(2)
outlier3 = Outlier(3)
subspace1 = Subspace(5, [1, 3, 6], [outlier3, outlier2])
subspace2 = Subspace(4, [1, 4, 5], [Outlier(1), outlier3])
subspace3 = Subspace(6, [0, 2, 9], [outlier2, outlier3, Outlier(9)])
sub1: Literal = Literal(subspace1)
sub2: Literal = Literal(subspace2)
sub3: Literal = Literal(subspace3)

level1: Operation = Operation(Operator.LOGICAL_AND, [sub1, sub2])
level2: Operation = Operation(Operator.LOGICAL_OR, [level1, level1])
level3: Operation(Operator.LOGICAL_OR, [level1, level2, sub3])  # (sub1 and sub2) or sub3


class TestSubspaceLogic(unittest.TestCase):

    def test_level2_subspaces(self):
        subspaces = level2.get_subspaces()
        self.assertIn(subspace1, subspaces)
        self.assertIn(subspace2, subspaces)
        self.assertEqual(len(subspaces), 2)

    def test_level3_subspaces(self):
        subspaces: set[Subspace] = level3.get_subspaces()
        self.assertIn(subspace1, subspaces)
        self.assertIn(subspace3, subspaces)
        self.assertIn(subspace2, subspaces)
        self.assertEqual(len(subspaces), 3)

    def test_literals_evaluate(self):
        self.assertEqual(np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 0]), sub1.evaluate())
        self.assertEqual(np.array([0, 1, 0, 1, 0, 0, 0, 0, 0, 0]), sub2.evaluate())
        self.assertEqual(np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 1]), sub3.evaluate())
