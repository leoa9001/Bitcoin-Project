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


# have input data in bytes
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

    hash = binascii.unhexlify("00")+hash

    # print("Step 4: " + str(binascii.hexlify(hash)).upper())
    # print()

    ripe = hash

    hasher = hashlib.sha256()
    hasher.update(hash)
    hash = hasher.digest()

    # print("Step 5: "+ (str(binascii.hexlify(hash)).upper()))
    # print()

    hasher = hashlib.sha256()
    hasher.update(hash)
    hash = hasher.digest()

    # print("Step 6: "+ str(binascii.hexlify(hash).upper()))
    # print()
    #
    # print("Step 7:" + str(binascii.hexlify(hash[0:4])).upper())
    #
    # print("Step4 RIPE: "+ str(binascii.hexlify(ripe)).upper())
    # print()

    final_address_bytes = ripe+hash[0:4]

    # print("Step 8: "+ str(binascii.hexlify(final_address_bytes)).upper())
    # print()
    encoded_final = base58.b58encode(final_address_bytes)

    print(encoded_final)


# PRGClass that should handle passing rand_func and would keep track of multiple calls. REDO
class PassPRG:
    __hash = None
    __last_hash_num = 0

    # passphrase must be a string
    def __init__(self, passphrase):
        h = hashlib.sha256()
        h.update(passphrase.encode("utf-8"))
        self.__hash = h.hexdigest()

    def randfunc(self, N):
        if N <= 0:
            raise ValueError
            return

        length = N // 32

        if N % 32 != 0:
            length += 1

        h = hashlib.sha256()
        h.update((str(self.__hash) + str(self.__last_hash_num)).encode("utf-8"))
        # print("Hashed value: "+ str(self.__hash)+str(self.__last_hash_num)+" N: "+str(N))
        PRG_Bytes = h.digest()
        self.__last_hash_num += 1

        for i in range(1, length):
            h = hashlib.sha256()
            h.update((str(self.__hash) + str(self.__last_hash_num)).encode("utf-8"))
            # print("Hashed value: "+ str(self.__hash)+str(self.__last_hash_num))
            PRG_Bytes = PRG_Bytes + h.digest()
            self.__last_hash_num += 1

        return PRG_Bytes[0:N]
