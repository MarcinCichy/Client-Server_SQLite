import os
import unittest
from server_package.user_management import UserManagement
import server_package.server_response as server_response
from server_package.database_support import DatabaseSupport
from server_package.user_authentication import UserAuthentication
import build_test_db

os.environ['TEST_ENV'] = 'test'
# os.environ['TEST_ENGINE'] = 'sqlite'
os.environ['TEST_ENGINE'] = 'postgresql'


class TestUserManagement(unittest.TestCase):

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
        self.usr_mgmt = UserManagement(self.database_support)
        self.user_auth = UserAuthentication(self.database_support)

    def test_user_list(self):
        build_test_db.drop_temp_db()
        build_test_db.create_temp_db()
        build_test_db.fill_temp_db()
        expected_result = {server_response.EXISTING_ACCOUNTS: {
            "user1": {"permissions": "admin", "status": "active"},
            "user2": {"permissions": "user", "status": "banned"},
            "user3": {"permissions": "user", "status": "active"},
            "user4": {"permissions": "admin", "status": "active"},
            "user5": {"permissions": "user", "status": "banned"}
            }
        }
        result = self.usr_mgmt.user_list()
        self.assertEqual(result, expected_result)

    def test_create_account_valid_data(self):
        self.usr_mgmt.user_del("jakito")  # Usuń użytkownika, jeśli istnieje
        new_account_data = [{'username': 'jakito'}, {'password': 'takion'}, {'permissions': 'user'}, {'status': 'active'}]
        result = self.usr_mgmt.create_account(new_account_data)
        self.assertEqual(result, server_response.NEW_ACCOUNT_CREATED)

    def test_create_account_exist_data(self):
        new_username = {'username': "user1"}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "user"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.usr_mgmt.create_account(data)
        self.assertEqual(result, server_response.E_ACCOUNT_EXIST)

    def test_create_account_invalid_username_data(self):
        new_username = {'username': ""}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "user"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.usr_mgmt.create_account(data)
        self.assertEqual(result, server_response.E_USER_NAME_NOT_PROVIDED)

    def test_create_account_invalid_permissions_data(self):
        new_username = {'username': "username2"}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "superuser"}  # Nieprawidłowe uprawnienia
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.usr_mgmt.create_account(data)
        self.assertEqual(result, server_response.E_WRONG_PERMISSIONS)

    def test_delete_user_valid_data(self):
        valid_user_to_del = "user4"
        result = self.usr_mgmt.user_del(valid_user_to_del)
        self.assertEqual(result, {valid_user_to_del: server_response.USER_DELETED})

    def test_delete_user_invalid_data(self):
        user_to_del = "user_100"
        result = self.usr_mgmt.user_del(user_to_del)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_delete_logged_user(self):
        user_to_del = "user1"  # Zakładam, że 'user1' jest zalogowany
        result = self.usr_mgmt.user_del(user_to_del)
        self.assertEqual(result, server_response.E_USER_LOGGED_CANNOT_BE_DELETED)

    def test_user_info_not_exist_user(self):
        not_exist_user_info = "username2"
        result = self.usr_mgmt.user_info(not_exist_user_info)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_change_user_permissions_no_data(self):
        data = []
        result = self.usr_mgmt.user_perm(data)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_change_user_permissions_no_user_exist(self):
        user_to_change_permission = 'username2'
        permissions_to_change = 'admin'
        data = {user_to_change_permission: permissions_to_change}
        result = self.usr_mgmt.user_perm(data)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_change_user_permissions_logged_user(self):
        valid_login_data = [{"username": "user1"}, {"password": "password1"}]
        self.user_auth.login(valid_login_data)
        user_to_change_permission = 'user1'
        permissions_to_change = 'user'
        data = {user_to_change_permission: permissions_to_change}
        result = self.usr_mgmt.user_perm(data)
        self.assertEqual(result, server_response.E_USER_LOGGED_CANNOT_CHANGE_PERMISSIONS)

    def test_change_user_permissions_wrong_new_permissions(self):
        user_to_change_permission = 'user3'
        permissions_to_change = 'other'
        data = {user_to_change_permission: permissions_to_change}
        result = self.usr_mgmt.user_perm(data)
        self.assertEqual(result, server_response.E_WRONG_PERMISSIONS)

    def test_change_user_permissions_valid_all_data(self):
        user_to_change_permission = 'user4'
        permissions_to_change = 'admin'
        data = {user_to_change_permission: permissions_to_change}
        result = self.usr_mgmt.user_perm(data)
        self.assertEqual(result, {user_to_change_permission: server_response.USER_PERMISSIONS_CHANGED})



    # Dodaj inne testy...

if __name__ == '__main__':
    unittest.main(verbosity=2)
