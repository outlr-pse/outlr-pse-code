import math
import unittest

import pandas as pd
import numpy as np
from pyod.utils import generate_data

from models.experiment import Experiment, Subspace
from models.subspacelogic import SubspaceLogic
from models.subspacelogic.literal import Literal
from models.subspacelogic.operation import Operation
from models.subspacelogic.operator import Operator
from models.dataset.dataset import Dataset
from models.user.user import User
from models.odm.pyodm import PyODM
import database.database_access as db
from execution.odm_scheduler.sequential_odm_scheduler import SequentialODMScheduler
from execution.experiment_scheduler.coroutine_experiment_scheduler import CoroutineExperimentScheduler
from models.base import Base


def setUpModule() -> None:
    Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    Base.metadata.create_all(bind=db.engine)
    db.setup_db()


class TestCoroutineSequentialScheduler(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(name="x", password="3232")
        db.add_user(self.user)
        self.odm = db.get_odm(1)
        self.odm.__class__ = PyODM
        self.odm_scheduler = SequentialODMScheduler()
        self.experiment_scheduler = CoroutineExperimentScheduler(self.odm_scheduler)

        self.contamination = 0.4  # percentage of outliers
        self.n_train = 200  # number of training points
        self.n_test = 0
        self.X_train, self.X_test, self.y_train, self.y_test = generate_data(
            n_train=self.n_train, n_test=self.n_test, contamination=self.contamination, random_state=999, n_features=3)

        self.dataset = Dataset(name="dataset", dataset=pd.DataFrame(self.X_train))
        self.true_outliers = self.y_train

        self.sub1 = Subspace(columns=[0, 1, 2])
        self.sub2 = Subspace(columns=[0, 1])
        self.sub3 = Subspace(columns=[0])
        self.experiment = Experiment(
            name="Expeeriment",
            user_id=self.user.id,
            dataset_size=self.dataset.dataset.shape[0],
            dataset=self.dataset,
            subspaces=[self.sub1, self.sub2, self.sub3],
            odm=self.odm,
            param_values={'contamination': 0.1, 'n_neighbors': math.floor(self.n_train / 2), 'method': 'fast'},
            true_outliers=self.true_outliers,
            subspace_logic=Operation(
                operator=Operator.LOGICAL_OR,
                operands=[
                    Literal(self.sub1),
                    Literal(self.sub2),
                    Literal(self.sub3)
                ]
            )
        )

    async def test_coroutine_sequential_scheduler(self):
        db.add_experiment(self.experiment)
        with db.session.no_autoflush:  # alternatively use db.session.autoflush = False
            await self.experiment_scheduler.schedule(self.experiment)
        self.assertIs(self.experiment.error_json, None, msg="Execution failed")
        db.add_experiment(self.experiment)
