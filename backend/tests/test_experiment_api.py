import json
import os.path
import unittest
import time
from pathlib import Path

from models.base import Base
from api import app, error
from api.experiment_api import _experiment_scheduler, data_path, remove_user_data
import database.database_access as db
from models.experiment import Experiment


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

    def test_validate_dataset(self):
        with self.client as c:
            username = "ValidateDataset"
            password = 'TestPasswordValid0!'
            response = c.post("/api/user/register",
                              json={'username': username, 'password': password})
            assert response.status_code == 200
            response_dict = response.get_json()
            access_token = response_dict.get("access_token")
            self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
            response = c.post("/api/experiment/validate-dataset", json={})
            response_dict = response.get_json()
            assert response_dict.get("error") == error.not_implemented.get("error")

    def test_validate_ground_truth(self):
        with self.client as c:
            username = "ValididateGroundtruth"
            password = 'TestPasswordValid0!'
            response = c.post("/api/user/register",
                              json={'username': username, 'password': password})
            assert response.status_code == 200
            response_dict = response.get_json()
            access_token = response_dict.get("access_token")
            self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
            response = c.post("/api/experiment/validate-ground-truth", json={})
            response_dict = response.get_json()
            assert response_dict.get("error") == error.not_implemented.get("error")

    def test_upload_experiment_files(self):
        """Testing file upload when dataset and groundtruth both passed"""
        username = "ValidDataUploadExperiments"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        response_dict = response.get_json()
        access_token = response_dict.get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        user_id: int
        with db.Session(expire_on_commit=False) as session:
            user = db.get_user(session, username)
            user_id = user.id
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'

        dataset_filename = 'dataset.csv'
        groundtruth_filename = 'groundtruth.csv'
        files = {'dataset': open(test_files / dataset_filename, "rb"),
                 'ground_truth': open(test_files / groundtruth_filename, "rb")}
        response = self.client.post("/api/experiment/upload-files", data=files)
        response_data = response.get_data()
        assert response.status_code == 200
        assert response_data == b"OK"

        saved_dataset_filename = 'dataset.csv'
        saved_groundtruth_filename = 'ground_truth.csv'
        dataset_path = data_path(user_id, "dataset")
        groundtruth_path = data_path(user_id, "ground_truth")
        # dataset file existent, thus not just user_files/2 returned
        assert dataset_path == f"user_files/{user_id}/{saved_dataset_filename}"
        # groundtruth file existent
        assert groundtruth_path == f"user_files/{user_id}/{saved_groundtruth_filename}"
        assert os.path.exists(data_path(user_id, "dataset")) is True
        assert os.path.exists(data_path(user_id, "ground_truth")) is True
        # removing the files from the path
        remove_user_data(user_id)
        assert os.path.exists(data_path(user_id, "dataset")) is False
        assert os.path.exists(data_path(user_id, "ground_truth")) is False

    def test_upload_experiment_files_no_groundtruth(self):
        username = "NoGroundTruth"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        response_dict = response.get_json()
        access_token = response_dict.get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        user_id: int
        with db.Session(expire_on_commit=False) as session:
            user = db.get_user(session, username)
            user_id = user.id
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'

        dataset_filename = 'dataset.csv'
        files = {'dataset': open(test_files / dataset_filename, "rb")}
        response = self.client.post("/api/experiment/upload-files", data=files)
        response_data = response.get_data()
        assert response.status_code == 200
        assert response_data == b"OK"

        assert os.path.exists(data_path(user_id, "dataset")) is True
        assert os.path.exists(data_path(user_id, "ground_truth")) is False
        # removing the files from the path
        remove_user_data(user_id)
        assert os.path.exists(data_path(user_id, "dataset")) is False
        assert os.path.exists(data_path(user_id, "ground_truth")) is False

    def test_upload_experiment_files_no_dataset(self):
        username = "NoDataset"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        response_dict = response.get_json()
        access_token = response_dict.get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        user_id: int
        with db.Session(expire_on_commit=False) as session:
            user = db.get_user(session, username)
            user_id = user.id
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'

        groundtruth_filename = 'groundtruth.csv'
        files = {'ground_truth': open(test_files / groundtruth_filename, "rb")}
        response = self.client.post("/api/experiment/upload-files", data=files)
        response_dict = response.get_json()
        assert "error" in response_dict
        assert response_dict.get("error") == error.no_dataset.get("error")
        assert os.path.exists(data_path(user_id, "dataset")) is False
        assert os.path.exists(data_path(user_id, "ground_truth")) is False
        # removing the files from the path
        remove_user_data(user_id)
        assert os.path.exists(data_path(user_id, "dataset")) is False
        assert os.path.exists(data_path(user_id, "ground_truth")) is False

    def test_count(self):
        # Account creation
        username = "Count1"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        access_token = response.get_json().get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        with self.client as c:
            response = c.get("/api/experiment/count")
            response_dict = response.get_json()
            assert response.status_code == 200
            assert response_dict.get("amount") == 0

    def test_create_experiment(self):
        # Account creation
        username = "CreateExperiment1"
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

        # uploading files nr 1
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'
        dataset_filename = 'dataset.csv'
        groundtruth_filename = 'groundtruth.csv'
        files = {'dataset': open(test_files / dataset_filename, "rb"),
                 'ground_truth': open(test_files / groundtruth_filename, "rb")}
        file_upload_response = self.client.post("/api/experiment/upload-files", data=files)
        assert file_upload_response.status_code == 200

        with open(file=test_files / "create_experiment.json", mode="r") as create_exp_json:
            create_exp_data = json.load(create_exp_json)
            with self.client as c:
                response = c.post("/api/experiment/create", json=create_exp_data)
                time.sleep(20)
                response_data = response.get_data()
                assert response.status_code == 200
                assert response_data == b"OK"

                with db.Session(expire_on_commit=False) as session:
                    exp_name = create_exp_data.get("name")
                    experiment = session.query(Experiment).filter_by(name=exp_name).first()
                    assert experiment is not None

                # After experiment execution dataset, ground truth are deleted
                assert os.path.exists(data_path(user_id, "dataset")) is False
                assert os.path.exists(data_path(user_id, "ground_truth")) is False

            with self.client as c:
                response = c.get("/api/experiment/count")
                response_dict = response.get_json()
                assert response.status_code == 200
                assert response_dict.get("amount") == 1

    def test_get_all(self):
        # Account creation
        username = "GetAll1"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        access_token = response.get_json().get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        # uploading files
        this_dir = Path(__file__).parent
        test_files = this_dir.parent / 'test_files'
        dataset_filename = 'dataset.csv'
        groundtruth_filename = 'groundtruth.csv'
        files = {'dataset': open(test_files / dataset_filename, "rb"),
                 'ground_truth': open(test_files / groundtruth_filename, "rb")}
        file_upload_response = self.client.post("/api/experiment/upload-files", data=files)
        assert file_upload_response.status_code == 200

        # experiment creation
        with open(file=test_files / "create_experiment.json", mode="r") as create_exp_json:
            create_exp_data = json.load(create_exp_json)
            with self.client as c:
                response = c.post("/api/experiment/create", json=create_exp_data)
                time.sleep(5)
                assert response.status_code == 200
                assert response.get_data() == b"OK"

        # uploading files #2
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
                time.sleep(5)
                assert response.status_code == 200
                assert response.get_data() == b"OK"

        with self.client as c:
            with open(file=test_files / "create_experiment.json", mode="r") as create_exp_json:
                create_exp_data = json.load(create_exp_json)
            response = c.get("/api/experiment/get-all")
            response_arr = response.get_json()
            assert len(response_arr) == 2
            for exp in response_arr:
                assert exp.get("name") == create_exp_data.get("name")
