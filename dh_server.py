from net.server import Server
from parsing.dh_parse import parse_server_argumets
from crypto.dh import DH
from asn import ASNCoder


def recv_client_params(srv):
    length = server.recv(7)
    params = server.recv(int.from_bytes(length, 'big'))
    p, g, A = ASNCoder.decode_dh_client(params)

    print('Client params')
    print(f'p = {p}\ng = {g}\nA = {A}')


if __name__ == '__main__':
    args = parse_server_argumets()
    server = Server(args.port)
    server.listen(1)
    server.accept()

    recv_client_params(server)

    server.close()
