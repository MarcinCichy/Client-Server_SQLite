import os
import unittest
from client_package.windows.handlers import Handlers


class TestClientHandlers(unittest.TestCase):
    def test_prepare_command_empty(self):
        self.assertEqual(Handlers.prepare_command("user", ""), {"user": None})

    def test_prepare_command_without_data(self):
        command = "help"
        expected = {"user": "help"}
        self.assertEqual(Handlers.prepare_command("user", command), expected)

    def test_prepare_command_user_del(self):
        command = "user-del to_delete_user"
        expected = {"user": {"user-del": "to_delete_user"}}
        self.assertEqual(Handlers.prepare_command("user", command), expected)

    def test_prepare_command_user_del_without_name_of_user_to_delete(self):
        command = "user-del"
        expected = {"user": {"user-del": None}}
        self.assertEqual(Handlers.prepare_command("user", command), expected)

    def test_prepare_command_user_stat(self):
        command = "user-stat anybody banned"
        expected = {"user": {"user-stat": {"anybody": "banned"}}}
        self.assertEqual(Handlers.prepare_command("user", command), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
