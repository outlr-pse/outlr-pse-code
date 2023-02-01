import unittest
import database.database_access as db
from database.database_access import session
from models.user.user import User
from models.experiment.experiment import Experiment
from models.odm.odm import ODM, HyperParameter
from models.base import Base


class TestDBAccess(unittest.TestCase):
    @classmethod
    def exp(cls, name: str, user_id: int) -> Experiment:
        """Create an experiment with the given name and user_id."""
        exp = Experiment()
        exp.user_id = user_id
        exp.name = name
        exp.subspace_logic = {"a": 1}
        exp.odm_params = {"b": 2}
        exp.true_outliers = [1, 2, 3]
        return exp

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.drop_all(bind=db.engine, checkfirst=True)
        Base.metadata.create_all(bind=db.engine)
        u = User(name="overleafer", password="nix")
        db.add_user(u)
        db.add_experiment(cls.exp("exp1", u.id))
        db.add_experiment(cls.exp("exp2", u.id))
        db.add_experiment(cls.exp("exp3", u.id))

    def test_add_experiment(self) -> None:
        exp = self.exp("exp4", 1)
        self.assertEqual(None, exp.id)
        db.add_experiment(exp)
        self.assertEqual(4, exp.id)

    def test_get_experiment(self) -> None:
        exp = db.get_experiment(1)
        self.assertEqual("exp1", exp.name)
        self.assertEqual(1, exp.id)

    def test_add_user(self) -> None:
        user = User(name="underleafer", password="nix")
        self.assertEqual(None, user.id)
        db.add_user(user)
        self.assertEqual(2, user.id)

    def test_get_user(self) -> None:
        user = db.get_user(1)
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
    #     self.assertEqual(1, odm.id)
    #     assert session.get(HyperParameter, 1).name == "hp1"
    #     assert session.get(HyperParameter, 2).name == "hp2"
    #     assert session.get(HyperParameter, 3).name == "hp3"
