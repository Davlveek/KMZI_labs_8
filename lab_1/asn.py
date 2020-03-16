import asn1


class ASNCoder:
    @staticmethod
    def encode(n, e, key, ciphertext):
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
        encoder.leave()

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

    @staticmethod
    def decode(filename):
        with open(filename, 'rb') as file:
            data = file.read()
            decoder = asn1.Decoder()
            decoder.start(data)
            ints = []
            ints = ASNCoder.asn_parse(decoder, ints)
            ciphertext = data[-ints[-1]:]  # Get ciphertext length and slice data
            return ints[0], ints[1], ints[2], ciphertext
