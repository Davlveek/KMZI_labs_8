from aes import AESCipher, AES_KEY_SIZE
from rsa import RSA
from asn import ASNCoder
from parse import parse_arguments
from privkey import *

PRIVKEY_FILE = 'privkey.py'


def form_privkey_file(d):
    params = f'privkey = {str(d)}\n'
    with open(PRIVKEY_FILE, 'w') as params_file:
        params_file.write(params)


def encrypt(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        key, ciphertext = AESCipher.encrypt(data)

        e, d, n = RSA.generate_params()
        form_privkey_file(d)
        encrypted_key = RSA.encrypt(int.from_bytes(key, 'big'), e, n)
        asn_encoded = ASNCoder.encode(n, e, encrypted_key, ciphertext)

        with open(f'{filename}.asn1', 'wb') as asn_file:
            asn_file.write(asn_encoded)


def decrypt(filename):
    n, e, encrypted_key, ciphertext = ASNCoder.decode(filename)
    key = RSA.decrypt(encrypted_key, privkey, n)
    plaintext = AESCipher.decrypt(
        ciphertext,
        key.to_bytes(AES_KEY_SIZE, 'big')
    )
    with open(f'{filename}.dec', 'wb') as file:
        file.write(plaintext)


if __name__ == '__main__':
    args = parse_arguments()
    if args.encrypt:
        encrypt(args.file)
    elif args.decrypt:
        decrypt(args.file)
