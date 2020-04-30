from Crypto.Random.random import randint
from Crypto.Util.number import isPrime, GCD, inverse
from datetime import datetime
from math import log


def gen_params(n):
    while True:
        a = randint(0, n - 1)
        x = randint(0, n - 1)
        y = randint(0, n - 1)
        b = (y ** 2 - x ** 3 - a * x) % n
        g = GCD(n, 4 * a ** 3 + 27 * b ** 2)
        if g == n:
            continue
        if g > 1:
            return None, None, None, None
        return a, b, x, y


def lenstra(n, m):
    cnt = 0
    while True:
        a, b, x, y = gen_params(n)
        if a is None:
            return None, None

        i = 0

        curve = [a, b]
        print(f'Curve: y^2 = x^3 + {a} * x + {b}')

        point = [x, y]
        print(f'Point: x = {x}, y = {y}')

        Q = [x, y]

        while i < m:
            if not isPrime(i):
                i += 1
                continue

            r = int((log(n, 2) / log(i, 2)) * (1 / 2))
            if r == 0:
                r = 1
            p = i ** r

            for j in range(1, p):
                cnt += 1
                if Q[0] == point[0] and Q[1] == point[1]:
                    numerator = (3 * Q[0] ** 2 + curve[0]) % n
                    denominator = inverse((2 * Q[1]), n)
                    L = numerator * denominator % n
                    if 1 < GCD(L, n) < n:
                        return GCD(L, n), cnt
                    x3 = (L ** 2 - 2 * Q[0]) % n
                    y3 = (L * (Q[0] - x3) - Q[1]) % n
                    Q[1] = y3
                    Q[0] = x3
                else:
                    numerator = (point[1] - Q[1]) % n
                    denominator = inverse((point[0] - Q[0]), n)
                    L = numerator * denominator % n
                    if 1 < GCD(L, n) < n:
                        return GCD(L, n), cnt
                    x3 = (L ** 2 - Q[0] - point[0]) % n
                    y3 = (L * (Q[0] - x3) - Q[1]) % n
                    Q[1] = y3
                    Q[0] = x3
                    if cnt % 10000000 == 0:
                        print(cnt)


def main():
    number = int(input('Enter number: '))
    base = int(input('Enter base: '))

    if not isPrime(number):
        start = datetime.now()
        p, iterations = lenstra(number, base)
        end = datetime.now()

        if p is None:
            return

        q = number // p
        print(f'{p} * {q} = {number}')
        print(f'p len: {p.bit_length()}')
        print(f'q len: {q.bit_length()}')
        print(f'{iterations} iterations')
        print(f'{end - start} worktime')
    else:
        print(f'{number} is prime number')


main()
