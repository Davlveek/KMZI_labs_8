from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

IV = b'\x00' * AES.block_size
AES_KEY_SIZE = 32


class AESCipher:
    @staticmethod
    def encrypt(data):
        key = get_random_bytes(AES_KEY_SIZE)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return key, ciphertext

    @staticmethod
    def encrypt_with_key(data, key):
        cipher = AES.new(key.to_bytes(AES_KEY_SIZE, 'big'), AES.MODE_CBC, IV)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        cipher = AES.new(key, AES.MODE_CBC, IV)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return data
