import argparse


def parse_client_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'server_ip',
        help='Server IP'
    )
    parser.add_argument(
        'server_port',
        type=int,
        help='Server port'
    )

    return parser.parse_args()


def parse_server_argumets():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'port',
        type=int,
        help='Listening port'
    )

    return parser.parse_args()
