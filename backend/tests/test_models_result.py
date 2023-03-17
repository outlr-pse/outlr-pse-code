import unittest
from datetime import datetime, timedelta

from models.experiment import ExperimentResult, Experiment, Subspace, Outlier
from models.subspacelogic.literal import Literal
from models.odm.pyodm import PyODM

exp = Experiment(id=123, creation_date=datetime.now())
res = ExperimentResult(
    id=12,
    accuracy=0.89,
    auc=0.9,
    fpr=[0, 0, 1],
    tpr=[0, 1, 1],
    execution_date=datetime.now(),
    execution_time=timedelta(minutes=2),
    experiment=exp
)
res_space = Subspace(id=2343, columns=None, name="result")
sub1 = Subspace(id=23, experiment=exp, columns=[0, 1, 3])
sub2 = Subspace(id=123, columns=[32])
res.result_space = res_space
exp.subspaces.append(sub2)
out1 = Outlier(index=3, subspaces=[sub1, sub2], experiment_result=res)
out2 = Outlier(index=4, experiment_result=res)
res.outliers.append(out1)
res.outliers.append(out2)
sub2.outliers.append(out2)


class TestResultModels(unittest.TestCase):

    def test_model_relations(self):
        self.assertIn(
            sub1, exp.subspaces,
            msg="Check if experiment contains subspace added with Subspace(experiment=...)"
        )

        self.assertIn(
            sub2, exp.subspaces,
            msg="Check if experiment contains subspace added manually to experiment.subspaces"
        )

        self.assertNotIn(
            res_space, exp.subspaces,
            msg="Check that result space is not in experiment.subspaces"
        )

        self.assertEqual(
            len(exp.subspaces), 2,
            msg="Check that experiment.subspaces does not contain more than expected"
        )

        self.assertIs(
            sub1.experiment, exp,
            msg="Check that subspace.experiment is correct when set manually in Subspace constructor"
        )

        self.assertIs(
            sub2.experiment, exp,
            msg="Check that subspace.experiment is correct when added by experiment.subspaces.append(subspace)"
        )

        self.assertIs(res_space.experiment, None, msg="Check that result_space.experiment is None")

        self.assertIn(
            out1, sub1.outliers,
            msg="Check that outlier is in subspace.outliers, when set in Outlier constructor"
        )

        self.assertIn(
            out1, sub2.outliers,
            msg="Check that outlier is in subspace.outliers, when set in Outlier constructor"
        )

        self.assertIn(
            out2, sub2.outliers,
            msg="Check that outlier is in subspace.outliers when added manually with subspace.outliers.appends(outlier)"
        )

        self.assertIn(
            sub1, out1.subspaces,
            msg="Check that subspace is in outlier.subspaces when added in Subspace constructor"
        )

        self.assertIn(
            sub2, out2.subspaces,
            msg="Check that subspace is in outlier.subspaces when added in Subspace constructor"
        )

        self.assertIn(
            sub2, out2.subspaces,
            msg="Check that subspace is in outlier.subspaces when added with subspace.outliers.append(outlier)"
        )

    def test_subspace_json(self):
        self.assertEqual(
            {"id": 23, "name": None, "columns": [0, 1, 3], "outliers": [3]},
            sub1.to_json()
        )

        self.assertEqual(
            {"id": 123, "name": None, "columns": [32], "outliers": [3, 4]},
            sub2.to_json()
        )

        self.assertEqual(
            {"id": 2343, "name": "result", "columns": [], "outliers": []},
            res_space.to_json()
        )

    def test_result_json(self):
        self.assertEqual(
            {
                "id": 12,
                "accuracy": 0.89,
                "auc": 0.9,
                "fpr": [0, 0, 1],
                "tpr": [0, 1, 1],
                "execution_date": res.execution_date.isoformat(),
                "execution_time": 2 * 1000000 * 60,
                "result_space": res_space.to_json()  # This is already tested by test_subspace_json()
            },
            res.to_json(True)
        )

    def test_subspace_from_json(self):
        _sub1 = Subspace.from_client_json(sub1.to_json())
        # See help(Subspace.from_client_json) to find out what attributes are read from the json
        self.assertEqual(_sub1.id, sub1.id)
        self.assertEqual(_sub1.columns, sub1.columns)
        self.assertEqual(_sub1.name, sub1.name)

    def test_subspace_logic(self):
        self.assertIn(sub1, exp.subspaces, msg="This is necessary for the following test case to work")
        exp.subspace_logic = Literal(sub1)
        self.assertIs(type(exp.subspace_logic), Literal)
        self.assertEqual(exp.subspace_logic.subspace.columns, sub1.columns)

    def test_experiment_from_json(self):
        exp_json = {
            "name": "test",
            "subspace_logic": {
                "literal": {
                    "subspace": {
                        "id": 23,
                        "name": None,
                        "columns": [0, 1, 3],
                        "outliers": [3],
                        "roc_curve": None
                    }
                }
            },
            "odm": {
                "id": 1,
                "hyper_parameters": {
                    "n_neighbors": 5
                },
            },
            "dataset_name": "test",
        }
        _exp = Experiment.from_json(exp_json)
        self.assertEqual(_exp.name, exp_json["name"])
        self.assertEqual(len(_exp.subspaces), 1)
        self.assertEqual(_exp.subspaces[0].columns, exp_json["subspace_logic"]["literal"]["subspace"]["columns"])
        self.assertEqual(_exp.odm_id, exp_json["odm"]["id"])
        self.assertEqual(_exp.param_values, exp_json["odm"]["hyper_parameters"])
        self.assertEqual(_exp.dataset_name, exp_json["dataset_name"])

    def test_experiment_to_json(self):
        exp.odm = PyODM(id=1)
        exp.param_values = {"n_neighbors": 5}
        exp_json_without_outliers = exp.to_json(False)
        self.assertEqual(exp_json_without_outliers["name"], exp.name)
        self.assertEqual(exp_json_without_outliers["odm_params"], exp.param_values)
        self.assertEqual(exp_json_without_outliers["dataset_name"], exp.dataset_name)
