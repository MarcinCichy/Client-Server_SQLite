# tests/unit/test_user_authentication.py

import os
import unittest
from server_package.user_authentication import UserAuthentication
import server_package.server_response as server_response
from server_package.database_support import DatabaseSupport
import build_test_db

os.environ['TEST_ENV'] = 'test'
# os.environ['TEST_ENGINE'] = 'sqlite'
os.environ['TEST_ENGINE'] = 'postgresql'


class TestUserAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Tworzymy i wypełniamy bazę danych raz przed uruchomieniem testów
        build_test_db.drop_temp_db()
        build_test_db.create_temp_db()
        build_test_db.fill_temp_db()

    @classmethod
    def tearDownClass(cls):
        # Usuwamy bazę danych po zakończeniu testów
        build_test_db.drop_temp_db()

    def setUp(self):
        self.database_support = DatabaseSupport()
        self.user_auth = UserAuthentication(self.database_support)

    def test_login_user_no_login_data(self):
        no_data = []
        result = self.user_auth.login(no_data)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_login_user_valid_data(self):
        valid_login_data = [{"username": "user1"}, {"password": "password1"}]
        expected = {"Login": "OK", "login_username": "user1", "user_permissions": "admin"}
        result = self.user_auth.login(valid_login_data)
        self.assertEqual(result, expected)

    def test_login_banned_user(self):
        banned_user_data = [{"username": "user2"}, {"password": "password2"}]
        expected = server_response.E_USER_IS_BANNED
        result = self.user_auth.login(banned_user_data)
        self.assertEqual(result, expected)

    # Dodaj inne testy...

if __name__ == '__main__':
    unittest.main(verbosity=2)
