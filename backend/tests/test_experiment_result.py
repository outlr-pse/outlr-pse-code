import json
import unittest
import time
from pathlib import Path

from models.base import Base
from api import app, error
from api.experiment_api import _experiment_scheduler
import database.database_access as db


def setUpModule() -> None:
    Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    Base.metadata.create_all(bind=db.engine)
    db.setup_db()


class TestExperimentApi(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.client.environ_base['HTTP_AUTHORIZATION'] = ""
        _experiment_scheduler.stop()

    def test_get_result_when_no_exp(self):
        # Account creation
        username = "GetResultNoExp1"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        access_token = response.get_json().get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        with self.client as c:
            response = c.get("/api/experiment/get-result/2")
            assert response.status_code == 404
            assert response.get_json().get("error") == error.no_experiment_with_id.get("error")
