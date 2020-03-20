from crypto.rsa import RSA, lower_border, upper_border, randprime, gcd


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
