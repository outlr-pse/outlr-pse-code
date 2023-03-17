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
        user_id: int
        with db.Session(expire_on_commit=False) as session:
            user = db.get_user(session, username)
            user_id = user.id

        with self.client as c:
            response = c.get("/api/experiment/get-result/2")
            assert response.status_code == 404
            assert response.get_json().get("error") == error.no_experiment_with_id.get("error")

    def test_get_result(self):
        # Account creation
        username = "GetResult1"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        access_token = response.get_json().get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        user_id: int
        with db.Session(expire_on_commit=False) as session:
            user = db.get_user(session, username)
            user_id = user.id

        # uploading files
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'
        dataset_filename = 'dataset.csv'
        groundtruth_filename = 'groundtruth.csv'
        files = {'dataset': open(test_files / dataset_filename, "rb"),
                 'ground_truth': open(test_files / groundtruth_filename, "rb")}
        file_upload_response = self.client.post("/api/experiment/upload-files", data=files)
        assert file_upload_response.status_code == 200

        # experiment creation #2
        with open(file=test_files / "create_experiment.json", mode="r") as create_exp_json:
            create_exp_data = json.load(create_exp_json)
            with self.client as c:
                response = c.post("/api/experiment/create", json=create_exp_data)
                time.sleep(4)
                assert response.status_code == 200
                assert response.get_data() == b"OK"

        with self.client as c:
            time.sleep(4)
            response = c.get("/api/experiment/get-result/1")
            assert response.status_code == 200
            response_dict = response.get_json()
            assert response_dict.get("experiment_result") is not None
            assert response_dict.get("experiment_result").get("result_space") is not None
            assert response_dict.get("name") is not None
            assert response_dict.get("odm") is not None
            assert response_dict.get("odm_params") is not None
            assert response_dict.get("subspace_logic") is not None