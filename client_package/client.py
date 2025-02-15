import json
import socket
from client_package import client_data


class Client:
    def __init__(self, srv_host, srv_port, srv_buff):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_buff = srv_buff

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_and_send(self, command):
        with self.create_socket() as s:
            s.connect((self.srv_host, int(self.srv_port)))
            s.sendall(command)
            return s.recv(self.srv_buff)

    def process_command(self, sentence):
        in_comm = self.input_command(sentence)
        try:
            response = self.connect_and_send(in_comm)
            return self.json_decode_received_data(response)
        except ConnectionError:
            return {"Error": "Unable to connect to server"}

    def input_command(self, command):
        encoded_command = self.json_serialize_command(command).encode(client_data.ENCODE_FORMAT)
        return encoded_command

    @staticmethod
    def json_serialize_command(comm):
        comm_dict = {"command": comm}
        comm_json = json.dumps(comm_dict)
        return comm_json

    @staticmethod
    def json_decode_received_data(data):
        decoded_data = json.loads(data)
        return decoded_data


def start(sentence):
    client = Client(client_data.HOST, client_data.PORT, client_data.BUFFER_SIZE)
    transmit = client.process_command(sentence)
    return transmit

