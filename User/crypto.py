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


# User sha256 from hashlib and return hexdigest (figure out how to make it work for arbitrary data though)
# def hash(path_to_data):


# have input data in bytes and it will return a string
def address(input_data_bytes):
    hasher = hashlib.sha256()
    hasher.update(input_data_bytes)
    hash = hasher.digest()
    # print("Step 2: ")
    # print(hasher.hexdigest().upper())
    # print()

    hasher = hashlib.new("ripemd160")
    hasher.update(hash)
    hash = hasher.digest()

    # print("Step 3: ")
    # print(hasher.hexdigest().upper())
    # print()

    hash = binascii.unhexlify("00") + hash

    # print("Step 4: " + str(binascii.hexlify(hash)).upper())
    # print()
    encoded_final = base58.b58encode_check(hash)

    # print((encoded_final).upper())

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
        h.update(bytes(passphrase, encoding = "utf-8"))
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
            # print("Generating w/ hashnum: "+ str(self.__last_hash_num))
            h = hashlib.sha256()
            h.update(self.__hash + bytes(self.__last_hash_num))
            self.__hash_bytes = self.__hash_bytes + h.digest()
            self.__last_hash_num += 1
