import unittest

from models.odm.odm import ODM
from models.odm.hyper_parameter import HyperParameter
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

# class TestODM(unittest.TestCase):
#     def setUp(self):
#         self.odm = ODM(id=1, name='test_odm', deprecated=False)
#
#     def test_to_json(self):
#         expected_result = {'id': 1, 'name': 'test_odm', 'hyper_parameters': [], 'deprecated': False}
#         self.assertDictEqual(self.odm.to_json(), expected_result)
#
#     def test_hyper_parameters(self):
#         hp1 = HyperParameter(id=1, name='hp1', value='value1')
#         hp2 = HyperParameter(id=2, name='hp2', value='value2')
#         self.odm.hyper_parameters = [hp1, hp2]
#
#         expected_hp_json = [hp1.to_json(), hp2.to_json()]
#         self.assertEqual(self.odm.to_json()['hyper_parameters'], expected_hp_json)


if __name__ == '__main__':
    unittest.main()
