from net.server import Server
from parsing.dh_parse import parse_server_argumets
from crypto.dh import DH
from asn import ASNCoder
from crypto.aes import AESCipher, AES_KEY_SIZE


def recv_client_params(server):
    length = server.recv(7)
    params = server.recv(int.from_bytes(length, 'big'))
    p, g, A = ASNCoder.decode_dh_client(params)

    print('Client params')
    print(f'p = {p}\ng = {g}\nA = {A}')

    return p, g, A


def send_server_params(server, B):
    asn_encoded = ASNCoder.encode_dh_server(B)
    length = len(asn_encoded)
    server.send(length.to_bytes(1, 'big'))
    server.send(asn_encoded)


def recv_msg(server, key):
    length = server.recv(7)
    asn_msg = server.recv(int.from_bytes(length, 'big'))
    ciphertext = ASNCoder.decode_dh_msg(asn_msg)
    plaintext = AESCipher.decrypt(ciphertext, key.to_bytes(AES_KEY_SIZE, 'big'))
    print(plaintext)


def main():
    args = parse_server_argumets()

    server = Server(args.port)
    server.listen(1)
    server.accept()

    p, g, A = recv_client_params(server)
    B, key = DH.generate_server_params(A, g, p)
    print(f'key = {key}')
    send_server_params(server, B)
    recv_msg(server, key)

    server.close()


if __name__ == '__main__':
    main()
