from Crypto.Hash import SHA256


def sha256(m):
    h = SHA256.new()
    h.update(m)
    return h.hexdigest()
