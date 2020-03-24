import socket


class Server:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.port))
        self.conn = None

    def listen(self, bakclog):
        self.sock.listen(bakclog)

    def accept(self):
        self.conn, addr = self.sock.accept()
        return addr

    def send(self):
        pass

    def recv(self, size):
        data = self.conn.recv(size)
        if not data:
            print('Invalid data')
            return None
        else:
            return data

    def close(self):
        pass
