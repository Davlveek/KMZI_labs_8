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
        asn_encoded = ASNCoder.encode_rsa(n, e, encrypted_key, ciphertext)

        with open(f'{filename}.asn1', 'wb') as asn_file:
            asn_file.write(asn_encoded)


def decrypt(filename):
    n, e, encrypted_key, ciphertext = ASNCoder.decode_rsa(filename)
    key = RSA.decrypt(encrypted_key, privkey, n)
    plaintext = AESCipher.decrypt(
        ciphertext,
        key.to_bytes(AES_KEY_SIZE, 'big')
    )
    with open(f'{filename}.dec', 'wb') as file:
        file.write(plaintext)


def form_sign(filename):
    with open(filename, 'rb') as file:
        data = file.read()

    e, d, n = RSA.generate_params()
    sign = RSA.sign(data, d, n)
    asn_encoded = ASNCoder.encode_rsa_sign(sign, e, n)

    with open(f'{filename}.sign.asn1', 'wb') as asn_file:
        asn_file.write(asn_encoded)


def check_sign(filename):
    with open(filename, 'rb') as file:
        data = file.read()

    n, e, sign = ASNCoder.decode_rsa_sign(f'{filename}.sign.asn1')

    if RSA.sign_check(data, sign, e, n):
        print('File is correct')
    else:
        print('File is incorrect')


if __name__ == '__main__':
    args = parse_arguments()
    if args.encrypt:
        encrypt(args.file)
    elif args.decrypt:
        decrypt(args.file)
    elif args.sign:
        form_sign(args.file)
    elif args.check:
        check_sign(args.file)