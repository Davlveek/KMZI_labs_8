import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        help='Input file'
    )
    parser.add_argument(
        '-e', '--encrypt',
        action='store_true',
        help='Encrypt file'
    )
    parser.add_argument(
        '-d', '--decrypt',
        action='store_true',
        help='Decrypt file'
    )

    return parser.parse_args()
