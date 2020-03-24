import socket


class Client:
    def __init__(self, ip: object, port: object) -> object:
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.server_ip, self.server_port))

    def send(self, data):
        self.sock.send(data)

    def recv(self):
        pass

    def close(self):
        self.sock.close()
