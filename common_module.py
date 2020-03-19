from crypto.rsa import RSA

def find_fs(N):
    f = 0
    while N % 2 == 0:
        N = N / 2
        f += 1
    return f, N


def find_t(b, n):
    l = 0
    while pow(b, pow(2, l)) % n != 1:
        l = + 1
    t = pow(b, pow(2, l - 1))
    return None if t % n == -1 else t


def generate():
    n, p, q = RSA.generate_module()

    while True:
        # Generate A params
        e_a, euler_func = RSA.generate_exp(p, q)
        d_a = RSA.mult_inv(e_a, euler_func)

        # Generate B params
        e_b, euler_func = RSA.generate_exp(p, q)
        d_b = RSA.mult_inv(e_b, euler_func)

        if e_b != e_a and d_b != d_a:
            return n, e_a, d_a, e_b, d_b


if __name__ == '__main__':
    n, e_a, d_a, e_b, d_b = generate()

    print(f'n = {n}')
    print('A params:')
    print(f'e = {e_a}\nd = {d_a}')
    print('B params:')
    print(f'e = {e_b}\nd = {d_b}')

    #N = e * d - 1
    #f, s = find_fs(N)
    #while True:
    #    a = random.randint(0, n - 1)
    #    b = pow(a, s, n)
    #    t = find_t(b, n)
    #    if t:
    #        break
    #
    #p = gcd(t + 1, n)
    #q = gcd(t - 1, n)
    #euler_func = (p - 1) * (q - 1)
