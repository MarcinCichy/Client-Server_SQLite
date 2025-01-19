import os
import unittest
from server_package.menu import CommandHandler
from server_package.functions import SystemUtilities
import server_package.server_response as server_response

os.environ['TEST_ENV'] = 'test'

class TestMenu(unittest.TestCase):
    def setUp(self):
        self.system_utilities = SystemUtilities()
        self.user_command_handler = CommandHandler()

    def test_help_command_with_user_permissions(self):
        user_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        # user_command_handler = CommandHandler()
        self.user_command_handler.user_data = user_data
        self.assertIn("uptime", self.user_command_handler.use_command({"marcin": "help"}, 'user'))

    def test_help_command_with_admin_permissions(self):
        admin_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = admin_data
        self.assertIn("user-add", user_command_handler.use_command({'admin_user': 'help'}, 'admin'))

    def test_help_command_with_unknown_permissions(self):
        unknown_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = unknown_data
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'help'}, 'unkknown'), server_response.E_WRONG_PERMISSIONS)

    def test_stop_command_with_user_permissions(self):
        user_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = user_data
        self.assertEqual(user_command_handler.use_command({"username": "stop"}, 'user'), server_response.E_COMMAND_UNAVAILABLE)

    def test_stop_command_with_admin_permissions(self):
        admin_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}, {'permissions': 'admin'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = admin_data
        self.assertEqual(user_command_handler.use_command({'admin_user': 'stop'}, 'admin'), {'Connection': 'close'})

    def test_stop_command_with_unknown_permissions(self):
        unknown_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = unknown_data
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'stop'}, 'unkknown'), server_response.E_COMMAND_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)

