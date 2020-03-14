from aes import AESCipher
from rsa import RSA
from asn import ASNCoder
from parse import parse_arguments
import struct


def encrypt(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        key, ciphertext = AESCipher.encrypt(data)


def decrypt():
    pass


if __name__ == '__main__':
    args = parse_arguments()
    if args.encrypt:
        encrypt(args.file)
    elif args.decrypt:
        pass
