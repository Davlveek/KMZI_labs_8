from crypto.rsa import RSA
from vuln_params import generate_small_order_params


def find_plaintext(mod, exp, c):
    i = 0
    c0 = c
    c = pow(c, exp, n)
    c_prev = c
    while True:
        c = pow(c, exp, n)
        if c == c0:
            return c_prev
        i += 1
        c_prev = c


if __name__ == '__main__':
    e, d, n = generate_small_order_params()
    print(f'n = {n}\ne = {e}\nd = {d}\n')
    plaintext = 412321432543655
    print(f'plaintext = {plaintext}')
    ciphertext = RSA.encrypt(plaintext, e, n)
    msg = find_plaintext(n, e, ciphertext)
    print(f'plaintext = {msg}')
