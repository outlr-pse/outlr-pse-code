import unittest

from models.ODM import HyperParameter, ODM
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


class TestHyperParameter(unittest.TestCase):
    def setUp(self):
        self.hyper_parameter = HyperParameter()
        self.hyper_parameter.id = 1
        self.hyper_parameter.name = "parameter_1"

    def test_to_json(self):
        expected_result = {
            "id": 1,
            "name": "parameter_1"
        }
        self.assertEqual(self.hyper_parameter.to_json(), expected_result)

class TestODM(unittest.TestCase):
    def setUp(self):
        self.odm = ODM(id=1, name='test_odm', deprecated=False)

    def test_to_json(self):
        expected_result = {'id': 1, 'name': 'test_odm'}
        self.assertDictEqual(self.odm.to_json(), expected_result)

    def test_attributes(self):
        self.assertEqual(self.odm.id, 1)
        self.assertEqual(self.odm.name, 'test_odm')
        self.assertEqual(self.odm.deprecated, False)


if __name__ == '__main__':
    unittest.main()
