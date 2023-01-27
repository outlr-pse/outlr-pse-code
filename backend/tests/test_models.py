import unittest
from models.user.user import User


# TODO: Add more tests for Experiment, ODM and User
class TestUser(unittest.TestCase):
    def test_deserialize(self):
        user_json = {
            "name": "overleafer"
        }

        user = User.from_json(user_json)
        user.id = 0
        user_json["id"] = user.id
        self.assertEqual(user.to_json(), user_json)
