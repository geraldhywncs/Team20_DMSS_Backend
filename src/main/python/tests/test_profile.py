import unittest
from utility.user_utility import User_Utility

class TestAddition(unittest.TestCase):
    def setUp(self):
        # Create a user instance before each test
        self.user = User_Utility.create_user("geraldhyw", "gerald@test.com", "password", "status" )

    def test_get_user(self):
        # create user first
        user = User_Utility.get_user(1)
        self.assertEqual(user.user_name, "geraldhyw")
        # self.assertEqual(user.first_name, "Gerald")
        # self.assertEqual(user.last_name, "Hoo")
        self.assertEqual(user.email, "gerald@test.com")

if __name__ == '__main__':
    unittest.main()