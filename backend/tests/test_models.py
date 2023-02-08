import unittest

from models.odm.odm import ODM
from models.odm.hyper_parameter import HyperParameter
from models.user.user import User


# TODO: Add more tests for Experiment, ODM and User
class TestUser(unittest.TestCase):
    def test_serialize(self):
        user_json = {
            "username": "overleafer",
            "access_token": "jwt"
        }

        user = User(name="overleafer")
        self.assertEqual(user.to_json("jwt"), user_json)


class TestHyperParameter(unittest.TestCase):
    def setUp(self):
        self.hp = HyperParameter(id=1, name='test_hp', param_type='int', optional=True)

    def test_to_json(self):
        expected_result = {'id': 1, 'name': 'test_hp', 'type': 'int', 'optional': True}
        self.assertDictEqual(self.hp.to_json(), expected_result)

    def test_attributes(self):
        self.assertEqual(self.hp.id, 1)
        self.assertEqual(self.hp.name, 'test_hp')
        self.assertEqual(self.hp.param_type, 'int')
        self.assertEqual(self.hp.optional, True)


class TestODM(unittest.TestCase):
    def setUp(self):
        self.odm = ODM(id=1, name='test_odm', deprecated=False)

    def test_to_json(self):
        expected_result = {'id': 1, 'name': 'test_odm', 'hyper_parameters': [], 'deprecated': False}
        self.assertDictEqual(self.odm.to_json(), expected_result)
        expected_result = {'id': 1, 'name': 'test_odm'}
        self.assertDictEqual(self.odm.to_json_no_params(), expected_result)

    def test_hyper_parameters(self):
        hp1 = HyperParameter(id=1, name='hp1')
        hp2 = HyperParameter(id=2, name='hp2')
        self.odm.hyper_parameters = [hp1, hp2]

        expected_hp_json = [hp1.to_json(), hp2.to_json()]
        self.assertEqual(self.odm.to_json()['hyper_parameters'], expected_hp_json)

    def test_attributes(self):
        self.assertEqual(self.odm.id, 1)
        self.assertEqual(self.odm.name, 'test_odm')
        self.assertEqual(self.odm.deprecated, False)
