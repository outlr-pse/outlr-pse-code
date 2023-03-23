import unittest

from backend.src.api.user_management_api import generate_password_hash, check_password_hash
from backend.src.api.experiment_api import _experiment_scheduler

class TestHashing(unittest.TestCase):

    def tearDown(self) -> None:
        _experiment_scheduler.stop()
    def test_correct_password(self):
        pw_one = "Test01&"
        pw_two = "Test02&!"
        pw_three = "ThisIsAThirdTestPassword018397240!"
        hash_one = generate_password_hash(pw_one)
        hash_two = generate_password_hash(pw_two)
        hash_three = generate_password_hash(pw_three)

        # test incorrect
        assert check_password_hash(hash_one.decode("utf-8"), pw_one + "!!") is False
        assert check_password_hash(hash_two.decode("utf-8"), pw_two + "!") is False
        assert check_password_hash(hash_three.decode("utf-8"), pw_three + "!") is False

        # test correct
        assert check_password_hash(hash_one.decode("utf-8"), pw_one) is True
        assert check_password_hash(hash_two.decode("utf-8"), pw_two) is True
        assert check_password_hash(hash_three.decode("utf-8"), pw_three) is True
    def test_wrong_password(self):
        password_hash = generate_password_hash("Test01&")
        password_hash_decoded = password_hash.decode("utf-8")
        passwords = ["testing123!(/)", "weirdwklglö", "ltiot4pu4p122", "poetiu6ui56jklth", "Ijegjh.l.",
                     "ipoturteilöwräp45", "!!69587568956"]
        for testpw in passwords:
            assert check_password_hash(password_hash_decoded, testpw) is False

