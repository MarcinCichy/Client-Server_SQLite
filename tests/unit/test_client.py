import os
import json
import unittest
from client_package.client import Client
import server_package.server_response as server_response
import server_package.server_data as server_data


class TestClientInitialization(unittest.TestCase):
    def setUp(self):
        self.test_host = "127.0.0.1"
        self.test_port = 8000
        self.test_buff = 1024
        self.client = Client(self.test_host, self.test_port, self.test_buff)

    def test_initialization(self):
        self.assertEqual(self.client.srv_host, self.test_host)
        self.assertEqual(self.client.srv_port, self.test_port)
        self.assertEqual(self.client.srv_buff, self.test_buff)


class TestClient(unittest.TestCase):
    def setUp(self):
        self.test_host = "127.0.0.1"
        self.test_port = 65432
        self.test_buff = 1024
        self.client = Client(self.test_host, self.test_port, self.test_buff)

    def dummy_connect_and_send(self, command):
        return json.dumps({'Unrecognised command': 'Please correct or type <help>.'}).encode()

    def test_handle_connection_unrecognised_command(self):
        self.client.connect_and_send = self.dummy_connect_and_send
        response = self.client.process_command({"command": "test"})
        expected_result = server_response.UNRECOGNISED_COMMAND
        self.assertEqual(response, expected_result)

    def test_handle_connection_valid_command(self):
        self.client.connect_and_send = lambda x: json.dumps({"response": "ok"}).encode()
        response = self.client.process_command({"command": "test"})
        self.assertEqual(response, {"response": "ok"})

    def test_handle_no_connection_to_server(self):
        self.client = Client("127.0.0.100", self.test_port, self.test_buff)
        result = self.client.process_command({"command": "info"})
        expected_result = {"Error": "Unable to connect to server"}
        self.assertEqual(result, expected_result)


class TestDataHandling(unittest.TestCase):
    def test_json_decode_received_data(self):
        test_data = json.dumps({"version": server_data.VERSION, "start_at": str(server_data.DATE)}).encode('utf-8')
        decoded_data = Client.json_decode_received_data(test_data)
        self.assertIn("version", decoded_data)

    def test_json_serialize_command(self):
        test_command = "test_command"
        serialized_command = Client.json_serialize_command(test_command)
        self.assertEqual(json.loads(serialized_command), {"command": test_command})

    def test_json_serialize_response_Stop_Server(self):
        test_response = {"Connection": "close"}
        serialized_command = Client.json_serialize_command(test_response)
        self.assertEqual(json.loads(serialized_command), {'command': test_response})


if __name__ == "__main__":
    unittest.main(verbosity=2)
