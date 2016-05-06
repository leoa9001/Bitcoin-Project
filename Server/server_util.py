import os
import simplejson as json
from blockchain import wallet
import datetime
from blockchain.util import APIException
import hashlib
import binascii
import base58

def get_apikey():
    file = open(os.path.expanduser("~") + "/.sppserver/apikey.txt", "r")
    apikey = file.read()
    file.close()
    return apikey


def get_passphrase():
    file = open(os.path.expanduser("~") + "/.sppserver/passphrase.txt", "r")
    passphrase = file.read()
    file.close()
    return passphrase


# Return current time as an integer
def get_current_time():
    return int(datetime.datetime.now().timestamp())


# Gets list of wallets (wallets made via create_wallet and definitely does not include Store wallet)
def get_wallet_list():
    wallets_file = open(os.path.expanduser("~") + "/.sppserver/wallets.txt", "r")
    wallets = []

    for line in wallets_file:
        if line[line.__len__() - 1] == "\n":
            wallets.append(line[0:line.__len__() - 1])
        else:
            wallets.append(line)

    wallets_file.close()
    return wallets


# Server utilities

# Main Wallet by default
def get_wallet(wallet_name="MainWallet"):
    wallet_file = open(os.path.expanduser("~") + "/.sppserver/Wallets/" + wallet_name + ".json")
    wallet_json = json.loads(wallet_file.read())
    wallet_file.close()

    if wallet_json["passphrase"] == "default":
        passphrase = get_passphrase()
    else:
        passphrase = wallet_json["passphrase"]
    return wallet.Wallet(identifier=wallet_json["identifier"], password=passphrase,
                         service_url="http://localhost:3000/", api_code=get_apikey())


# Should return the transaction hash:
def private_publish(hash, address, wallet_name="MainWallet"):
    if not address(hash)==address:
        raise Exception("Invalid address and or hash.")

    wallet = get_wallet(wallet_name)
    try:
        response = wallet.send(to=address, amount=5461)
    except APIException as e:
        print("API response: ")
        print(e.args)
        return "failed private publish"

    # Write in data here
    file = open(os.path.expanduser("~") + "/.sppserver/Publishes/" + wallet_name + "/tx_hash_list.txt", "a")
    file.write(response.tx_hash + "\n")
    file.close()

    data_json = {
        "Wallet": wallet_name,
        "address": address,
        "time": get_current_time(),
        "tx_hash": response.tx_hash
    }
    # Rewrite this youf ool!
    file = open(os.path.expanduser("~") + "/.sppserver/Publishes/" + wallet_name + "/Publishmetas/" + address + ".json", "w")
    file.write(json.dumps(data_json))
    file.close()

    return response.tx_hash


def get_donation_address(wallet_name="MainWallet"):
    wallet = get_wallet(wallet_name)
    return wallet.new_address(label="Donation Address").address


def get_balance(wallet_name="MainWallet"):
    return get_wallet(wallet_name).get_balance()

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
