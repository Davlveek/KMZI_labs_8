from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

iv = b'\x00' * AES.block_size


class AESCipher:
    @staticmethod
    def encrypt(data):
        key = get_random_bytes(AES.key_size[-1])  # Key size is 32
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return key, ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return data
