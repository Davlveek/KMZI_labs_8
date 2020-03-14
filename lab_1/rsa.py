class RSA:
    @staticmethod
    def encrypt(m, e, n):
        return pow(m, e, n)

    @staticmethod
    def decrypt(c, d, n):
        return pow(c, d, n)
