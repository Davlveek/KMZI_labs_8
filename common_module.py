import random
from sympy import gcd
from crypto.rsa import RSA


def find_fs(N):
    f = 0
    while N % 2 == 0:
        N = N // 2
        f += 1
    return f, N


def find_t(b, mod):
    l = 0
    while pow(b, pow(2, l)) % mod != 1:
        l += 1
    if l == 0:
        return None
    t = pow(b, pow(2, l - 1))
    return None if t % mod == -1 else t


def find_privkey(exp_a, exp_b, priv_b, mod):
    N = exp_b * priv_b - 1
    f, s = find_fs(N)
    while True:
        a = random.randint(0, mod - 1)
        b = pow(a, s, mod)
        t = find_t(b, mod)
        if t:
            break

    p = gcd(t + 1, mod)
    q = gcd(t - 1, mod)
    euler_func = (p - 1) * (q - 1)

    priv_a = RSA.mult_inv(exp_a, int(euler_func))
    print(f'Privkey = {priv_a}')


if __name__ == '__main__':
    n, e_a, d_a, e_b, d_b = RSA.generate_one_module_params()

    print(f'n = {n}')
    print('A params:')
    print(f'e = {e_a}\nd = {d_a}')
    print('B params:')
    print(f'e = {e_b}\nd = {d_b}')

    find_privkey(e_a, e_b, d_b, n)
