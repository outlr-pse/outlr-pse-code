# import unittest

# from user_management_api import generate_password_hash, check_password_hash
# from backend.src.api.experiment_api import _experiment_scheduler

# def tearDown() -> None:
#    _experiment_scheduler.stop()

# class TestHashing(unittest.TestCase):

#    def tearDown(self) -> None:
#        _experiment_scheduler.stop()

#    @unittest.skip("To be tested locally")
#    def test_correct_password(self):
#        pw_one = "Test01&"
#        pw_two = "Test02&!"
#        pw_three = "ThisIsAThirdTestPassword018397240!"
#        hash_one = generate_password_hash(pw_one)
#        hash_two = generate_password_hash(pw_two)
#        hash_three = generate_password_hash(pw_three)

# test incorrect
#       hash_one_decoded = hash_one.decode("utf-8")
#       assert check_password_hash(hash_one_decoded, pw_one + "!!") is False
#       hash_two_decoded = hash_two.decode("utf-8")
#       assert check_password_hash(hash_two_decoded, pw_two + "!") is False
#       hash_three_decoded = hash_three.decode("utf-8")
#       assert check_password_hash(hash_three_decoded, pw_three + "!") is False

# test correct
#        assert check_password_hash(hash_one_decoded, pw_one) is True
#        assert check_password_hash(hash_two_decoded, pw_two) is True
#        assert check_password_hash(hash_three_decoded, pw_three) is True

#   @unittest.skip("To be tested locally")
#    def test_wrong_password(self):
#        password_hash = generate_password_hash("Test01&")
#        password_hash_decoded = password_hash.decode("utf-8")
#        passwords = ["testing123!(/)", "weirdwklglö", "ltiot4pu4p122",
#                       "poetiu6ui56jklth", "Ijegjh.l.",
#                     "ipoturteilöwräp45", "!!69587568956"]
#        for testpw in passwords:
#            assert check_password_hash(password_hash_decoded, testpw) is False
