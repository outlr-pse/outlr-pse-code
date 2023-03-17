import unittest

from models.base import Base
from api import app
from api.experiment_api import _experiment_scheduler
import database.database_access as db
from models.odm import ODM


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

    def test_for_odms(self):
        username = "AllODMs"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200

        access_token = response.get_json().get("access_token")

        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        response = self.client.get("api/odm/get-all")
        assert response.status_code == 200
        response_arr = response.get_json()
        all_odms: list
        with db.Session() as session:
            all_odms = db.get_all_odms(session)

        for odm in response_arr:
            in_all_odms = False
            for actual_odm in all_odms:
                if actual_odm.id == odm.get("id") and actual_odm.name == odm.get("name"):
                    in_all_odms = True
                    break
            assert in_all_odms is True

    def test_get_odm_params(self):
        username = "GetODMParams"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200

        access_token = response.get_json().get("access_token")

        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        #looking for abod.ABOD
        odm_name = "abod.ABOD"
        odm_id: int
        odm: ODM
        with db.Session() as session:
            odm = session.query(ODM).filter_by(name=odm_name).first()
            odm_id = odm.id
        response = self.client.get(f"api/odm/get-parameters/{odm_id}")
        assert response.status_code == 200
        response_dict = response.get_json()
        for param in response_dict:
            assert param.get("id") is not None
            assert param.get("name") is not None
            assert param.get("optional") is not None
            assert param.get("type") is not None
