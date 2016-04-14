# Should handle everything that needs crypto primitives:
# Key generation and signing mostly.
#
import Crypto
import hashlib

def key_gen(passphrase, dummy = False):
    if dummy is None:
        return ("dummyprivatekey", "dummypublickey")

    # The irony of this line though; will fix it with actual crypto primitives
    return ("dummyprivatekey", "dummypublickey")


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
class MultiPRG:
    __hash = None
    __lasthashnum = 0

    def __init__(self, hash):
        self.__hash = hash

    # def randfunc(self):


