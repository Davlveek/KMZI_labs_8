from sympy import randprime, gcd
from crypto.hash import sha256

lower_border = pow(2, 511)
upper_border = pow(2, 512)


class RSA:
    @staticmethod
    def encrypt(m, e, n):
        return pow(m, e, n)

    @staticmethod
    def decrypt(c, d, n):
        return pow(c, d, n)

    @staticmethod
    def sign(m, d, n):
        r = sha256(m)
        return RSA.encrypt(int(r, 16), d, n)

    @staticmethod
    def sign_check(m, sign, e, n):
        s = RSA.decrypt(sign, e, n)
        r = sha256(m)
        return True if int(r, 16) == s else False

    @staticmethod
    def generate_exp(p, q):
        euler_func = (p - 1) * (q - 1)
        for e in range(lower_border, upper_border):
            if gcd(e, euler_func) == 1:
                return e, euler_func

    @staticmethod
    def mult_inv(e, euler_func):
        return pow(e, -1, euler_func)

    @staticmethod
    def generate_module():
        p = randprime(lower_border, upper_border)
        q = randprime(lower_border, upper_border)
        return p * q, p, q

    @staticmethod
    def generate_params():
        n, p, q = RSA.generate_module()
        e, euler_func = RSA.generate_exp(p, q)
        d = RSA.mult_inv(e, euler_func)
        return e, d, n
