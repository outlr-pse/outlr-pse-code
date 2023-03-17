import unittest

from api import error
from api import app
from api.user_management_api import validate_username, validate_password
from models.base import Base
import database.database_access as db
from api.experiment_api import  _experiment_scheduler


def setUpModule() -> None:
    Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    Base.metadata.create_all(bind=db.engine)
    db.setup_db()


class TestUserManagementAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.client.environ_base['HTTP_AUTHORIZATION'] = ""
        _experiment_scheduler.stop()

    def test_register_valid_data(self):
        """Tests registering a user with valid username and password"""
        username = "ValidData01"
        password = 'TestPasswordValid0!'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 200
        response_dict = response.get_json()
        assert "username" in response_dict
        assert response_dict.get("username") == username
        assert "access_token" in response_dict
        assert "error" not in response_dict

    def test_register_invalid_username(self):
        """Tests registering a user with invalid username"""
        username = "*hilkdsfskdfkjlffjdkglöi28o3u4rlgh21"
        password = 'TestPasswordValid0!'

        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 401
        response_dict = response.get_json()
        assert "username" not in response_dict
        assert "access_token" not in response_dict
        assert "error" in response_dict
        assert response_dict.get("error") == error.invalid_username.get("error")

    def test_register_invalid_password(self):
        """Tests registering a user with invalid password"""
        username = "SCH3LOM0"
        password = 'H&k____'
        response = self.client.post("/api/user/register",
                                    json={'username': username, 'password': password})
        assert response.status_code == 401
        response_dict = response.get_json()
        assert "username" not in response_dict
        assert "access_token" not in response_dict
        assert "error" in response_dict
        assert response_dict.get("error") == error.invalid_password.get("error")

    def test_register_username_taken(self):
        """Tests registering a user with username already taken"""
        # First register expected to be succesful as data is valid
        username = "ValidUser1"
        password = 'TestPasswordValid0!'
        response_first_register = self.client.post("/api/user/register",
                                                   json={'username': username, 'password': password})
        assert response_first_register.status_code == 200

        # Second register expected to fail as account with username already created
        username = "ValidUser1"
        password = 'TestPasswordValid0!'
        response_second_register = self.client.post("/api/user/register",
                                                    json={'username': username, 'password': password})
        # username was already taken
        assert response_second_register.status_code == error.username_already_taken.get("status")
        response_dict = response_second_register.get_json()
        assert "username" not in response_dict
        assert "access_token" not in response_dict
        assert "error" in response_dict
        assert response_dict.get("error") == error.username_already_taken.get("error")

    def test_login_valid_data(self):
        """Tests logging in with valid credentials"""
        username = "ValidLoginUser1"
        password = 'TestPasswordValid0!'
        register_response = self.client.post("/api/user/register",
                                             json={'username': username, 'password': password})
        assert register_response.status_code == 200

        login_response = self.client.post("/api/user/login",
                                          json={'username': username, 'password': password})
        assert login_response.status_code == 200
        response_dict = login_response.get_json()
        assert "error" not in response_dict
        assert "username" in response_dict
        assert response_dict.get("username") == username
        assert "access_token" in response_dict

    def test_login_invalid_credentials(self):

        response = self.client.post("/api/user/login",
                                    json={})
        response_dict = response.get_json()
        assert response_dict.get("error") == error.no_data_provided.get("error")

    def test_login_no_username(self):

        response = self.client.post("/api/user/login",
                                    json={})
        response_dict = response.get_json()
        assert response_dict.get("error") == error.no_data_provided.get("error")

    def test_login_no_password(self):
        password = "ValidPassword01!"
        response = self.client.post("/api/user/login",
                                    json={'password': password})
        response_dict = response.get_json()
        assert response_dict.get("error") == error.no_username_provided.get("error")

    def test_login_no_password(self):
        username = "TestUser1"
        response = self.client.post("/api/user/login",
                                    json={'username': username})
        response_dict = response.get_json()
        assert response_dict.get("error") == error.no_password_provided.get("error")

    def test_login_non_existent_user(self):
        username = "DoesNotExist"
        password = "Test01!"
        response = self.client.post("/api/user/login",
                                    json={'username': username, 'password': password})
        response_dict = response.get_json()
        assert response_dict.get("error") == error.provided_credentials_wrong.get("error")
        
    def test_login_invalid_data(self):
        """Tests logging in with false credentials"""
        username = "InvalidLoginUser1"
        password = 'TestPasswordValid0!'
        register_response = self.client.post("/api/user/register",
                                             json={'username': username, 'password': password})
        assert register_response.status_code == 200

        login_response = self.client.post("/api/user/login",
                                          json={'username': username, 'password': password + "1"})
        assert login_response.status_code == error.provided_credentials_wrong.get("status")
        response_dict = login_response.get_json()
        assert "username" not in response_dict
        assert "access_token" not in response_dict
        assert "error" in response_dict
        assert response_dict.get("error") == error.provided_credentials_wrong.get("error")

    def test_logout_success(self):
        """Tests logging out when actually logged in"""
        username = "LogoutUser1"
        password = 'TestPasswordValid0!'
        register_response = self.client.post("/api/user/register",
                                             json={'username': username, 'password': password})
        assert register_response.status_code == 200

        login_response = self.client.post("/api/user/login",
                                          json={'username': username, 'password': password})
        assert login_response.status_code == 200
        response_dict = login_response.get_json()
        assert "error" not in response_dict
        assert "username" in response_dict
        assert "access_token" in response_dict
        access_token = response_dict.get("access_token")
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        logout_response = self.client.post("/api/user/logout",
                                           json={'username': username, 'password': password})
        assert logout_response.status_code == 200

    def test_logout_no_success(self):
        """Tests logging out when not logged in"""
        username = "LogoutUser1"
        password = 'TestPasswordValid0!'
        access_token = "0"
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        logout_response = self.client.post("/api/user/logout",
                                           json={'username': username, 'password': password})
        assert logout_response.status_code == error.token_not_valid.get("status")
        response_dict = logout_response.get_json()
        assert "error" in response_dict
        assert response_dict.get("error") == error.token_not_valid.get("error")

    def test_get_token_identity_success(self):
        """Tests getting the user connected to a token when valid token passed, thus success"""
        username = "GetTokenIdentity01"
        password = 'TestPasswordValid0!'
        register_response = self.client.post("/api/user/register",
                                             json={'username': username, 'password': password})
        assert register_response.status_code == 200
        register_response_dict = register_response.get_json()
        assert "access_token" in register_response_dict
        access_token = register_response_dict.get("access_token")

        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        response = self.client.get("/api/user/get-token-identity")
        assert response.status_code == 202
        response_dict = response.get_json()
        assert "username" in response_dict
        assert "access_token" in response_dict
        assert response_dict.get("access_token") == access_token
        assert response_dict.get("username") == username

    def test_get_token_identity_no_success(self):
        """Tests getting the user connected to a token when no valid token passed"""
        response = self.client.get("/api/user/get-token-identity")
        assert response.status_code == error.token_not_valid.get("status")
        response_dict = response.get_json()
        assert "error" in response_dict
        assert response_dict.get("error") == error.token_not_valid.get("error")

    def test_validate_username_none(self):
        """Tests if the get token method returns None"""
        assert validate_username(None) is False

    def test_validate_password_none(self):
        """Tests if the get token method returns None"""
        assert validate_password(None) is False
