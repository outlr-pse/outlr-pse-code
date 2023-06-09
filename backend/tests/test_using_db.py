import unittest
from datetime import timedelta, datetime

import numpy as np

import database.database_access as db
from models.user import User
from models.experiment import Experiment, ExperimentResult, Subspace, Outlier
from models.subspacelogic.literal import Literal
from models.subspacelogic.operation import Operation, Operator
from models.odm import HyperParameter
from models.base import Base


def setUpModule() -> None:
    Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    Base.metadata.create_all(bind=db.engine)
    db.setup_db()


class TestDBAccess(unittest.TestCase):
    @classmethod
    def exp(cls, name: str, user_id: int) -> Experiment:
        """Create an experiment with the given name and user_id."""
        exp = Experiment()
        exp.user_id = user_id
        exp.creation_date = datetime.now()
        exp.name = name
        exp.odm_id = 1
        exp.odm_params = {"b": 2}
        exp.ground_truth = np.array([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1])
        exp.dataset_name = "datasatasat"
        outlier = Outlier(index=2)
        exp.subspaces = [Subspace(name="one subspace", columns=[1], outliers=[outlier])]
        exp.subspace_logic = Literal(exp.subspaces[0])
        exp.experiment_result = ExperimentResult(
            accuracy=0.89,
            execution_date=datetime.now(),
            execution_time=timedelta(minutes=2),
            outliers=[outlier],
            result_space=Subspace(name="result", outliers=[outlier])
        )
        return exp

    @classmethod
    def setUpClass(cls) -> None:
        with db.Session() as session:
            u = User(name="overleafer", password="nix")
            db.add_user(session, u)
            db.add_experiment(session, cls.exp("exp1", u.id))
            db.add_experiment(session, cls.exp("exp2", u.id))
            db.add_experiment(session, cls.exp("exp3", u.id))

    def test_add_experiment(self) -> None:
        with db.Session() as session:
            exp = self.exp("exp4", 1)
            self.assertEqual(None, exp.id)
            db.add_experiment(session, exp)
            self.assertEqual(4, exp.id)

    def test_get_experiment(self) -> None:
        with db.Session() as session:
            exp = db.get_experiment(session, user_id=1, exp_id=1)
            self.assertEqual("exp1", exp.name)
            self.assertEqual(1, exp.id)

    def test_add_user(self) -> None:
        with db.Session() as session:
            user = User(name="underleafer", password="nix")
            self.assertEqual(None, user.id)
            db.add_user(session, user)
            self.assertEqual(2, user.id)

    def test_get_user(self) -> None:
        with db.Session() as session:
            user = db.get_user(session, user=1)
            self.assertEqual("overleafer", user.name)
            self.assertEqual(1, user.id)

            exps = user.experiments
            self.assertEqual("exp1", exps[0].name)
            self.assertEqual("exp2", exps[1].name)
            self.assertEqual("exp3", exps[2].name)

    @classmethod
    def hp(cls, name: str) -> HyperParameter:
        hp = HyperParameter()
        hp.name = name
        return hp

    # def test_add_and_get_odm(self) -> None:
    #     odm = ODM()
    #     odm.name = "odm1"
    #     odm.hyper_parameters = [self.hp(hp) for hp in ["hp1", "hp2", "hp3"]]
    #     db.add_odm(odm)
    #     id0 = odm.hyper_parameters[0].id
    #     id1 = odm.hyper_parameters[1].id
    #     id2 = odm.hyper_parameters[2].id
    #     self.assertEqual(session.get(HyperParameter, id0).name, "hp1")
    #     self.assertEqual(session.get(HyperParameter, id1).name, "hp2")
    #     self.assertEqual(session.get(HyperParameter, id2).name, "hp3")


class TestODMProvider(unittest.TestCase):
    def test_scraper(self):
        with db.Session() as session:
            odms = db.get_all_odms(session)
            odm_names = [odm.name for odm in odms]
            self.assertIn('cd.CD', odm_names)
            self.assertIn('hbos.HBOS', odm_names)
            self.assertIn('anogan.AnoGAN', odm_names)
            self.assertIn('abod.ABOD', odm_names)
            self.assertIn('alad.ALAD', odm_names)
            self.assertIn('rod.ROD', odm_names)
            self.assertIn('knn.KNN', odm_names)
            db.setup_db()


class TestExperimentWithResult(unittest.TestCase):

    def test_experiment_with_result(self):
        with db.Session() as session:
            u = User(name="overleafer", password="nix")
            db.add_user(session, u)
            user_id = u.id

        with db.Session() as session:
            self.exp = Experiment(
                user_id=user_id,
                name="Experiment #1203",
                odm_id=1,
                creation_date=datetime.now(),
            )
            self.res = ExperimentResult(
                user_id=user_id,
                experiment=self.exp,
                accuracy=0.89,
                execution_date=datetime.now(), execution_time=timedelta(minutes=2)
            )
            self.res_space = Subspace(
                columns=None, name="result", outliers=[Outlier(index=111, experiment_result=self.res)]
            )
            self.sub1 = Subspace(columns=[0, 1, 3])
            self.exp.subspaces.append(self.sub1)
            self.sub2 = Subspace(columns=[32])
            self.res.result_space = self.res_space
            self.exp.subspaces.append(self.sub2)
            self.out1 = Outlier(index=3, subspaces=[self.sub1, self.sub2])
            self.out2 = Outlier(index=4)
            self.res.outliers.append(self.out1)
            self.res.outliers.append(self.out2)
            self.sub2.outliers.append(self.out2)
            self.exp.subspace_logic = Operation(
                operator=Operator.LOGICAL_AND,
                operands=[Literal(self.sub1), Literal(self.sub2), Literal(self.sub1)]
            )

            db.add_experiment(session, self.exp)
            self.assertEqual(1, 1, msg="Assert that the code doesn't raise an exception")
