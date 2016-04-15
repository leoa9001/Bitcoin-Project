# Should handle everything that needs crypto primitives:
# Key generation and signing mostly.
#
from Crypto.PublicKey import RSA as RSA
import hashlib


# Style change; keep it as string format or PyCrypto RSA key format?
def key_gen(passphrase, dummy=False):
    if dummy is True:
        return ("dummyprivatekey", "dummypublickey")

    full_key = RSA.generate(2048, randfunc = PassPRG(passphrase).randfunc)

    public_key = full_key.publickey()

    # PEM Format string representations: (Private key, Public key)
    return (full_key.exportKey(), public_key.exportkey())


# User sha256 from hashlib and return hexdigest (figure out how to make it work for arbitrary data though)
# def hash(data):




# Basically a class that will keep all of the functionality of an asymmetric encryption scheme that SPP will need
# in a neat format (if you change the scheme would only need to change the class and key_gen)
# class KeyPair:
#     __data = None
#
#     def __init__(self, passphrase):
#

# PRGClass that should handle passing rand_func and would keep track of multiple calls.
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
            h.update((str(self.__hash)+ str(self.__last_hash_num)).encode("utf-8"))
            print("Hashed value: "+ str(self.__hash)+str(self.__last_hash_num))
            PRG_Bytes  = PRG_Bytes+h.digest()
            self.__last_hash_num += 1

        return PRG_Bytes[0:N]