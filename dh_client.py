from net.client import Client
from parsing.dh_parse import parse_client_arguments
from crypto.dh import DH
from asn import ASNCoder


def send_dh_params(clnt):
    p, g, A = DH.generate_client_params()
    print(f'p = {p}\ng = {g}\nA = {A}')

    asn_encoded = ASNCoder.encode_dh_client(A, g, p)
    length = len(asn_encoded)
    clnt.send(length.to_bytes(1, 'big'))
    clnt.send(asn_encoded)


if __name__ == '__main__':
    args = parse_client_arguments()
    client = Client(args.server_ip, args.server_port)
    client.connect()
    send_dh_params(client)

    client.close()
