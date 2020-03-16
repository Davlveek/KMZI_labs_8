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
    parser.add_argument(
        '-s', '--sign',
        action='store_true',
        help='Sign file'
    )
    parser.add_argument(
        '-c', '--check',
        action='store_true',
        help='Check file sign'
    )

    return parser.parse_args()
