# Should handle everything that needs crypto primitives:
# Key generation and signing mostly.
#
from Crypto.PublicKey import RSA as RSA
import hashlib
import binascii
import base58


# Style change; keep it as string format or PyCrypto RSA key format?
def key_gen(passphrase, dummy=False):
    if dummy is True:
        return ("dummyprivatekey", "dummypublickey")

    full_key = RSA.generate(2048, randfunc=PassPRG(passphrase).randfunc)

    public_key = full_key.publickey()

    # PEM Format string representations: (Private key, Public key)
    return (full_key.exportKey(format="DER"), public_key.exportKey(format="DER"))





# have input data in bytes and it will return a string
def address(input_data_bytes):

    #Do it twice for valid address hacks.
    hasher = hashlib.sha256()
    hasher.update(input_data_bytes)
    hash = hasher.digest()

    hasher = hashlib.sha256()
    hasher.update(hash)
    hash = hasher.digest()

    hasher = hashlib.new("ripemd160")
    hasher.update(hash)
    hash = hasher.digest()

    hash = binascii.unhexlify("00") + hash

    encoded_final = base58.b58encode_check(hash)


    return encoded_final


# PRGClass that should handle passing rand_func and would keep track of multiple calls. REDO
class PassPRG:
    __hash = None
    __last_hash_num = 0
    __byte_index = 0
    __hash_bytes = bytes()

    # passphrase must be a string
    def __init__(self, passphrase):
        h = hashlib.sha256()
        h.update(bytes(passphrase, encoding="utf-8"))
        self.__hash = h.digest()

    def randfunc(self, N):
        if N <= 0:
            raise ValueError
            return

        byte_gen = N - 32 * self.__last_hash_num + self.__byte_index
        num_hashes = (byte_gen) // 32

        if byte_gen % 32 != 0:
            num_hashes += 1

        self.generate(num_hashes)

        self.__byte_index += N

        return self.__hash_bytes[self.__byte_index - N:self.__byte_index]

    def generate(self, num_hashes):
        for i in range(0, num_hashes):
            h = hashlib.sha256()
            h.update(self.__hash + bytes(self.__last_hash_num))
            self.__hash_bytes = self.__hash_bytes + h.digest()
            self.__last_hash_num += 1
