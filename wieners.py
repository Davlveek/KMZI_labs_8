import math
from crypto.rsa import RSA


def get_continued_fraction(exp, mod, l):
    a, q = divmod(exp, mod)
    t = mod
    res = [a]
    for i in range(0, l):
        if q == 0:
            break
        next_t = q
        a, q = divmod(t, q)
        t = next_t
        res.append(a)
    return res


def find_privkey(exp, mod):
    l = int(math.log2(mod))
    frac = get_continued_fraction(exp, mod, l)

    test_msg = 42314324324532324
    q_2 = 0
    q_1 = 1
    for a in frac[1:]:
        q = a * q_1 + q_2
        if pow(test_msg, exp * q, mod) == test_msg:
            print(f'privkey = {q}')
            return
        q_2 = q_1
        q_1 = q

    print("Wiener's attack failed")


if __name__ == '__main__':
    e, d, n = RSA.generate_wieners_params()
    print(f'n = {n}\ne = {e}\nd = {d}\n')
    if e != 0:
        find_privkey(e, n)
    else:
        print("Incorrect Wiener's params")
