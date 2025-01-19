import os
import json
import unittest
from server_package.server import Server
import server_package.server_response as server_response

os.environ['TEST_ENV'] = 'test'

class TestServerInitialization(unittest.TestCase):
    def setUp(self):
        self.test_host = "127.0.0.1"
        self.test_port = 8000
        self.test_buff = 1024
        self.server = Server(self.test_host, self.test_port, self.test_buff)

    def test_initialization(self):
        self.assertEqual(self.server.srv_host, self.test_host)
        self.assertEqual(self.server.srv_port, self.test_port)
        self.assertEqual(self.server.srv_buff, self.test_buff)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.test_host = "127.0.0.1"
        self.test_port = 8000
        self.test_buff = 1024
        self.server = Server(self.test_host, self.test_port, self.test_buff)

    def test_handle_connection_unrecognised_command(self):
        test_data = {"command": {"RECIPIENT": "inforrr"}}
        result = self.server.handle_connection(test_data, {"permissions": 'admin'})
        result_dict = json.loads(result)
        expected_result = server_response.UNRECOGNISED_COMMAND
        self.assertEqual(result_dict, expected_result)

    def test_handle_connection_correct_command(self):
        test_data = {"RECIPIENT": "info"}
        result = self.server.handle_connection(test_data, {"permissions": 'admin'})
        result_dict = json.loads(result)
        expected_result = "version"
        self.assertIn(expected_result, result_dict)

    def test_handle_connection_stop_command(self):
        test_data = {"marcin": "stop"}
        result = self.server.handle_connection(test_data, {"permissions": 'admin'})
        result_dict = json.loads(result)
        expected_result = {"Connection": "close"}
        self.assertEqual(expected_result, result_dict)

    def test_handle_connection_stop_command_invalid_permissions(self):
        test_data = {"logged_username": "stop"}
        result = self.server.handle_connection(test_data, {"permissions": 'user'})
        result_dict = json.loads(result)
        expected_result = server_response.E_COMMAND_UNAVAILABLE
        self.assertEqual(expected_result, result_dict)


class TestDataHandling(unittest.TestCase):
    def test_json_decode_received_data(self):
        test_data = json.dumps({"command": "test_command"}).encode('utf-8')
        decoded_data = Server.json_decode_received_data(test_data)
        self.assertEqual(decoded_data, "test_command")

    def test_json_serialize_response(self):
        test_response = {"status": "success"}
        serialized_response = Server.json_serialize_response(test_response)
        self.assertEqual(json.loads(serialized_response), test_response)

    def test_json_serialize_response_Stop_Server(self):
        test_response = {"Connection": "close"}
        serialized_response = Server.json_serialize_response(test_response)
        self.assertEqual(json.loads(serialized_response), test_response)


if __name__ == '__main__':
    unittest.main(verbosity=2)
