from random import randint
from sympy import randprime

lower_border = pow(2, 255)
upper_border = pow(2, 256)


class DH:
    @staticmethod
    def primitive_root(p, q_list):
        g = randint(2, p - 1)
        for q in q_list:
            if pow(g, (p - 1) // q, p) == 1:
                return DH.primitive_root(p, q_list)
        return g

    @staticmethod
    def generate_client_params():
        p = randprime(lower_border, upper_border)
        g = randint(2, p - 1)
        a = randint(2, p - 1)
        return p, g, pow(g, a)

    @staticmethod
    def generate_server_params():
        pass
