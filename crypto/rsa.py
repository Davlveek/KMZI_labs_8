import math
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
        for e in range(1000, euler_func - 1):
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

    @staticmethod
    def generate_one_module_params():
        n, p, q = RSA.generate_module()

        euler_func = (p - 1) * (q - 1)
        a_find = False
        e_a = e_b = 0
        for e in range(1000, euler_func - 1):
            if gcd(e, euler_func) == 1:
                if a_find:
                    e_b = e
                    break
                else:
                    e_a = e
                    a_find = True

        d_a = RSA.mult_inv(e_a, euler_func)
        d_b = RSA.mult_inv(e_b, euler_func)

        return n, e_a, d_a, e_b, d_b

    @staticmethod
    def generate_wieners_params():
        while True:
            p = randprime(lower_border, upper_border)
            q = randprime(lower_border, upper_border)
            if q < p < 2 * q:
                break
        n = p * q
        euler_func = (p - 1) * (q - 1)

        d = randprime(pow(2, 127), pow(2, 128))
        e = RSA.mult_inv(d, euler_func)
        if gcd(e, euler_func) == 1:
            return e, d, n
        else:
            return 0, 0, 0
