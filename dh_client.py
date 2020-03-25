from net.client import Client
from parsing.dh_parse import parse_client_arguments
from crypto.dh import DH
from asn import ASNCoder
from crypto.aes import AESCipher


def send_dh_params(client, p, g, A):
    asn_encoded = ASNCoder.encode_dh_client(A, g, p)
    length = len(asn_encoded)
    client.send(length.to_bytes(1, 'big'))
    client.send(asn_encoded)


def recv_server_params(client):
    length = client.recv(7)
    params = client.recv(int.from_bytes(length, 'big'))
    B = ASNCoder.decode_dh_server(params)

    print('Server params')
    print(f'B = {B}')

    return B


def send_file_data(client, filename, key):
    with open(filename, 'rb') as file:
        data = file.read()

    ciphertext = AESCipher.encrypt_with_key(data, key)
    asn_encoded = ASNCoder.encode_dh_msg(ciphertext)

    length = len(asn_encoded)
    client.send(length.to_bytes(1, 'big'))
    client.send(asn_encoded)


def main():
    args = parse_client_arguments()

    client = Client(args.server_ip, args.server_port)
    client.connect()

    a, p, g, A = DH.generate_client_params()
    print(f'a = {a}\np = {p}\ng = {g}\nA = {A}')

    send_dh_params(client, p, g, A)
    B = recv_server_params(client)

    key = pow(B, a, p)
    print(f'key = {key}')

    send_file_data(client, args.file, key)

    client.close()


if __name__ == '__main__':
    main()
