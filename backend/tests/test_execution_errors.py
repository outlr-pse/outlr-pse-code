import unittest

from models.experiment import Experiment, Subspace
from execution.execution_error import ExecutionError
from execution.execution_error.subspace_error import SubspaceError
from execution.execution_error.unknown_odm_error import UnknownODMError


class TestExecutionError(unittest.TestCase):

    def test_subspace_error(self):
        error = SubspaceError()
        experiment = Experiment(error_json=error.to_json())
        self.assertEqual(experiment.error_json, {"SubspaceError": {}})
        self.assertEqual(error.debug_message, "SubspaceError: A column index of a subspace was out of bounds")

    def test_base_execution_error(self):
        error = ExecutionError(debug_message="test")
        experiment = Experiment(error_json=error.to_json())
        self.assertEqual(experiment.error_json, {"ExecutionError": {"debug_msg": "test"}})
        self.assertEqual(error.debug_message, "ExecutionError: test")

    def test_unknown_odm_error(self):
        error = UnknownODMError(odm_name="test.TestODM")
        experiment = Experiment(error_json=error.to_json())
        self.assertEqual(experiment.error_json, {"UnknownODMError": {"odm_name": "test.TestODM"}})
        self.assertEqual(error.debug_message, "UnknownODMError: ODM test.TestODM does not exist")
