import unittest
import numpy as np

from models.subspacelogic import SubspaceLogic
from models.subspacelogic.literal import Literal
from models.subspacelogic.operation import Operation
from models.subspacelogic.operator import Operator
from models.experiment.experiment import Subspace, Outlier


# don't modify these variables
outlier2 = Outlier(index=2)
outlier3 = Outlier(index=3)
subspace1 = Subspace(id=12, columns=[1, 3, 6], outliers=[outlier3, outlier2])
subspace2 = Subspace(id=1231, columns=[1, 4, 5], outliers=[Outlier(index=1), outlier3])
subspace3 = Subspace(id=0, columns=[0, 2, 9], outliers=[outlier2, outlier3, Outlier(index=9)])
sub1: Literal = Literal(subspace1)
sub2: Literal = Literal(subspace2)
sub3: Literal = Literal(subspace3)

level1: Operation = Operation(Operator.LOGICAL_AND, [sub1, sub2])
level2: Operation = Operation(Operator.LOGICAL_OR, [level1, level1])
level3: Operation = Operation(Operator.LOGICAL_OR, [level1, level2, sub3])  # (sub1 and sub2) or sub3


def expected_json_subspace(sub: Subspace):
    return {
        "literal": {
            "subspace": sub.to_json()
        }
    }


expected_layer1 = {
    "operation": {
        "operator": "and",
        "operands": [expected_json_subspace(sub1.subspace), expected_json_subspace(sub2.subspace)]
    }
}
expected_layer2 = {
    "operation": {
        "operator": "or",
        "operands": [expected_layer1, expected_layer1]
    }
}
expected_layer3 = {
    "operation": {
        "operator": "or",
        "operands": [
            expected_layer1,
            expected_layer2,
            expected_json_subspace(sub3.subspace)
        ]
    }
}


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
        self.assertTrue((np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 0]) == sub1.evaluate(10)).all())
        self.assertTrue((np.array([0, 1, 0, 1, 0, 0, 0, 0, 0, 0]) == sub2.evaluate(10)).all())
        self.assertTrue((np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 1]) == sub3.evaluate(10)).all())

    def test_client_json(self):
        # Check literals
        self.assertEqual(sub1.to_client_json(), expected_json_subspace(sub1.subspace))
        self.assertEqual(sub2.to_client_json(), expected_json_subspace(sub2.subspace))
        self.assertEqual(sub3.to_client_json(), expected_json_subspace(sub3.subspace))
        # Check operations
        self.assertEqual(level1.to_client_json(), expected_layer1)
        self.assertEqual(level2.to_client_json(), expected_layer2)
        self.assertEqual(level3.to_client_json(), expected_layer3)

    def test_from_client_json(self):
        sub1_json = {
            "literal": {
                "subspace": {
                    "columns": [0, 12, 3, 3],
                    "name": "sub1"
                }
            }
        }
        sub2_json = {
            "literal": {
                "subspace": {
                    "columns": [0],
                    "name": "sub2"
                }
            }
        }
        sub3_json = {
            "literal": {
                "subspace": {
                    "columns": [0, 1, 3, 4, 325],
                }
            }
        }
        level_json = {
            "operation": {
                "operator": "and",
                "operands": [
                    sub1_json,
                    sub2_json,
                    sub3_json
                ]
            }
        }

        subspaces: dict[frozenset, Subspace] = {}
        _sub1 = SubspaceLogic.from_client_json(sub1_json, subspaces)
        _subspace1: Subspace = next(iter(subspaces.values()))
        _sub2 = SubspaceLogic.from_client_json(sub2_json, subspaces)
        _sub3 = SubspaceLogic.from_client_json(sub3_json, subspaces)
        _level = SubspaceLogic.from_client_json(level_json, subspaces)

        self.assertEqual(3, len(subspaces), msg="Check that existing_subspaces dict has been used correctly")
        self.assertIs(
            _subspace1, _level.operands[0].subspace,
            msg="Check that subspace has been reused"
        )

        # Test literals
        self.assertEqual(_sub1.subspace.name, "sub1")
        self.assertEqual(_sub1.subspace.columns, [0, 3, 12])
        self.assertEqual(_sub2.subspace.name, "sub2")
        self.assertEqual(_sub2.subspace.columns, [0])
        self.assertIs(_sub3.subspace.name, None)
        self.assertEqual(_sub3.subspace.columns, [0, 1, 3, 4, 325])
        # Test operations
        self.assertEqual(_level.operator, Operator.LOGICAL_AND)

    def test_database_json(self):
        sub1_json = {"l": {"s": sub1.subspace.id}}
        sub2_json = {"l": {"s": sub2.subspace.id}}
        sub3_json = {"l": {"s": sub3.subspace.id}}
        level1_json = {
            "o": {
                "f": level1.operator.json_name,
                "a": [sub1_json, sub2_json]
            }
        }
        level2_json = {
            "o": {
                "f": level2.operator.json_name,
                "a": [level1_json, level1_json]
            }
        }
        level3_json = {
            "o": {
                "f": level3.operator.json_name,
                "a": [level1_json, level2_json, sub3_json]
            }
        }
        self.assertEqual(sub1.to_database_json(), sub1_json)
        self.assertEqual(sub2.to_database_json(), sub2_json)
        self.assertEqual(sub3.to_database_json(), sub3_json)
        self.assertEqual(level1.to_database_json(), level1_json)
        self.assertEqual(level2.to_database_json(), level2_json)
        self.assertEqual(level3.to_database_json(), level3_json)

        subspaces = {sub.subspace.id: sub.subspace for sub in [sub1, sub2, sub3]}
        _sub1 = SubspaceLogic.from_database_json(sub1_json, subspaces)
        _sub2 = SubspaceLogic.from_database_json(sub2_json, subspaces)
        _sub3 = SubspaceLogic.from_database_json(sub3_json, subspaces)
        _level1 = SubspaceLogic.from_database_json(level1_json, subspaces)
        _level2 = SubspaceLogic.from_database_json(level2_json, subspaces)
        _level3 = SubspaceLogic.from_database_json(level3_json, subspaces)
        self.assertEqual(_sub1.to_database_json(), sub1_json)
        self.assertEqual(_sub2.to_database_json(), sub2_json)
        self.assertEqual(_sub3.to_database_json(), sub3_json)
        self.assertEqual(_level1.to_database_json(), level1_json)
        self.assertEqual(_level2.to_database_json(), level2_json)
        self.assertEqual(_level3.to_database_json(), level3_json)
