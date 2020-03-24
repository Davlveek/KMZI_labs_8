import asn1


class ASNCoder:
    @staticmethod
    def encode_dh_client(A, g, p):
        encoder = asn1.Encoder()
        encoder.start()

        encoder.enter(asn1.Numbers.Sequence)
        encoder.enter(asn1.Numbers.Set)
        encoder.enter(asn1.Numbers.Sequence)

        encoder.write(b'\x00\x21', asn1.Numbers.OctetString)  # DH identifeier
        encoder.write(b'dh', asn1.Numbers.UTF8String)

        encoder.enter(asn1.Numbers.Sequence)
        encoder.leave()

        # Cryptosystem params
        encoder.enter(asn1.Numbers.Sequence)
        encoder.write(p, asn1.Numbers.Integer)
        encoder.write(g, asn1.Numbers.Integer)
        encoder.leave()

        # Ciphertext (A param)
        encoder.enter(asn1.Numbers.Sequence)
        encoder.write(A, asn1.Numbers.Integer)
        encoder.leave()

        encoder.leave()
        encoder.leave()

        encoder.enter(asn1.Numbers.Sequence)
        encoder.leave()

        encoder.leave()

        return encoder.output()

    @staticmethod
    def encode_rsa(n, e, key, ciphertext):
        encoder = asn1.Encoder()
        encoder.start()

        encoder.enter(asn1.Numbers.Sequence)  # Sequence 1 (main)

        encoder.enter(asn1.Numbers.Set)  # Set - RSA keys
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 2

        # RSA params
        encoder.write(b'\x00\x01', asn1.Numbers.OctetString)  # RSA identifier
        encoder.write(b'\x0c\x00', asn1.Numbers.UTF8String)
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 3
        encoder.write(n, asn1.Numbers.Integer)
        encoder.write(e, asn1.Numbers.Integer)
        encoder.leave()  # End sequence 3

        # AES encrypted key
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 4
        encoder.write(key, asn1.Numbers.Integer)
        encoder.leave()  # End sequence 4

        encoder.leave()  # End sequence 2
        encoder.leave()  # End set

        # Cipher params
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 5
        encoder.write(b'\x10\x82', asn1.Numbers.OctetString)  # AES CBC identifier
        encoder.write(len(ciphertext), asn1.Numbers.Integer)
        encoder.leave()  # End sequence 5

        encoder.leave()  # End sequence 1

        encoder.write(ciphertext)

        return encoder.output()

    @staticmethod
    def decode_rsa(filename):
        with open(filename, 'rb') as file:
            data = file.read()
            decoder = asn1.Decoder()
            decoder.start(data)
            ints = []
            ints = ASNCoder.asn_parse(decoder, ints)
            ciphertext = data[-ints[-1]:]  # Get ciphertext length and slice data
            return ints[0], ints[1], ints[2], ciphertext

    @staticmethod
    def encode_rsa_sign(sign, e, n):
        encoder = asn1.Encoder()
        encoder.start()

        encoder.enter(asn1.Numbers.Sequence)  # Sequence 1

        encoder.enter(asn1.Numbers.Set)  # Set 1
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 2

        encoder.write(b'\x00\x40', asn1.Numbers.OctetString)  # RSA-SHA256
        encoder.write(b'\x0C\x00', asn1.Numbers.UTF8String)

        # RSA sign params
        encoder.enter(asn1.Numbers.Sequence)  # Sequence 3
        encoder.write(n, asn1.Numbers.Integer)
        encoder.write(e, asn1.Numbers.Integer)
        encoder.leave()  # End sequence 3

        encoder.enter(asn1.Numbers.Sequence)  # Sequence 4
        encoder.leave()  # End sequence 4

        encoder.enter(asn1.Numbers.Sequence)  # Sequence 5
        encoder.write(sign, asn1.Numbers.Integer)
        encoder.leave()  # End sequence 5

        encoder.leave()  # End sequence 2
        encoder.leave()  # End set 1

        encoder.enter(asn1.Numbers.Sequence)  # Sequence 6
        encoder.leave()  # End sequence 6

        encoder.leave()  # End Sequence 1

        return encoder.output()

    @staticmethod
    def decode_rsa_sign(sing_filename):
        with open(sing_filename, 'rb') as sign_file:
            data = sign_file.read()
            decoder = asn1.Decoder()
            decoder.start(data)
            ints = []
            ints = ASNCoder.asn_parse(decoder, ints)
            return ints[0], ints[1], ints[2]

    @staticmethod
    def decode_dh_client(data):
        decoder = asn1.Decoder()
        decoder.start(data)
        ints = []
        ints = ASNCoder.asn_parse(decoder, ints)
        return ints[0], ints[1], ints[2]

    @staticmethod
    def asn_parse(decoder, ints):
        while not decoder.eof():
            try:
                tag = decoder.peek()
                if tag.nr == asn1.Numbers.Null:
                    break
                if tag.typ == asn1.Types.Primitive:
                    tag, value = decoder.read()
                    if tag.nr == asn1.Numbers.Integer:
                        ints.append(value)
                elif tag.typ == asn1.Types.Constructed:
                    decoder.enter()
                    ASNCoder.asn_parse(decoder, ints)
                    decoder.leave()
            except asn1.Error:
                print("Can't parse file")
                break

        return ints
