import math
import unittest
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pandas as pd
from pyod.utils import generate_data

from models.experiment import Experiment, Subspace
from models.subspacelogic.literal import Literal
from models.subspacelogic.operation import Operation
from models.subspacelogic.operator import Operator
from models.user import User
from models.odm.pyodm import PyODM
import database.database_access as db
from execution.odm_scheduler import ODMScheduler
from execution.odm_scheduler.sequential_odm_scheduler import SequentialODMScheduler
from execution.odm_scheduler.executor_odm_scheduler import ExecutorODMScheduler
from execution.experiment_scheduler.background_thread_event_loop_experiment_scheduler \
    import BackgroundThreadEventLoopExperimentScheduler
from execution.experiment_scheduler.event_loop_experiment_scheduler import EventLoopExperimentScheduler
from models.base import Base


def setUpModule() -> None:
    Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    Base.metadata.create_all(bind=db.engine)
    db.setup_db()


class TestEventLoopScheduler(unittest.TestCase):

    def setUp(self) -> None:
        with db.Session(expire_on_commit=False) as session:
            self.user = User(name="x", password="3232")
            db.add_user(session, self.user)
            self.odm = db.get_odm(session, 1)
            self.odm.__class__ = PyODM
            self.odm_scheduler = SequentialODMScheduler()
            self.experiment_scheduler = BackgroundThreadEventLoopExperimentScheduler(self.odm_scheduler)

            self.contamination = 0.4  # percentage of outliers
            self.n_train = 200  # number of training points
            self.n_test = 0
            self.X_train, self.X_test, self.y_train, self.y_test = generate_data(
                n_train=self.n_train, n_test=self.n_test, contamination=self.contamination, random_state=999, n_features=3)

            self.dataset = pd.DataFrame(self.X_train)
            self.ground_truth = self.y_train

            self.sub1 = Subspace(columns=[0, 1, 2], outliers=[])
            self.sub2 = Subspace(columns=[0, 1], outliers=[])
            self.sub3 = Subspace(columns=[0], outliers=[])
            self.experiment = Experiment(
                name="Expeeriment",
                user_id=self.user.id,
                dataset=self.dataset,
                subspaces=[self.sub1, self.sub2, self.sub3],
                odm=self.odm,
                param_values={'contamination': 0.1, 'n_neighbors': math.ceil(self.n_train / 4), 'method': 'fast'},
                ground_truth=self.ground_truth,
                subspace_logic=Operation(
                    operator=Operator.LOGICAL_OR,
                    operands=[
                        Literal(self.sub1),
                        Literal(self.sub2),
                        Literal(self.sub3)
                    ]
                )
            )
            db.add_experiment(session, self.experiment)

    def tearDown(self) -> None:
        if isinstance(self.experiment_scheduler, EventLoopExperimentScheduler):
            self.experiment_scheduler.stop()  # Ensures that also on failing tests the loop is stopped

    def run_test_with_odm_scheduler(self, odm_scheduler: ODMScheduler):
        self.experiment_scheduler.odm_scheduler = odm_scheduler
        self.experiment_scheduler.schedule(self.experiment).result()
        self.assertIs(self.experiment.error_json, None, msg="Execution failed")
        with db.Session() as session:  # Check that the execution doesn't mess with the session
            session.add(self.experiment)
            session.commit()

    def test_coroutine_thread_scheduler_with_less_processes_than_subspaces(self):
        self.run_test_with_odm_scheduler(
            ExecutorODMScheduler(ProcessPoolExecutor(max_workers=len(self.experiment.subspaces) - 1))
        )

    def test_coroutine_thread_scheduler_with_less_threads_than_subspaces(self):
        self.run_test_with_odm_scheduler(
            ExecutorODMScheduler(ThreadPoolExecutor(max_workers=len(self.experiment.subspaces) - 1))
        )

    def test_coroutine_sequential_scheduler(self):
        self.run_test_with_odm_scheduler(SequentialODMScheduler())

    def test_odm_failure(self):
        self.experiment.param_values['method'] = 'invalid'  # This is no a valid hyperparameter value
        self.experiment_scheduler = BackgroundThreadEventLoopExperimentScheduler(
            ExecutorODMScheduler(ThreadPoolExecutor(max_workers=10))
        )
        self.experiment_scheduler.schedule(self.experiment).result()
        self.assertIsNot(self.experiment.error_json, None, msg="Execution error is missing")
        self.assertEqual(
            list(self.experiment.error_json.keys()), ["ODMFailureError"],
            msg="Execution error has wrong type"
        )
        with db.Session() as session:  # Check that the execution doesn't mess with the session
            session.add(self.experiment)
            session.commit()
