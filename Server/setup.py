import os
from blockchain.exceptions import APIException
from blockchain import createwallet
import sys
from Server import server_util
import simplejson as json


# Sets main folder and such
def setup(apikey, passphrase, settings=None):
    home_dir = os.path.expanduser("~")
    if os.path.exists(home_dir + "/.sppserver"):
        print("SPP Server has already been set up.")
        return

    main_dir = home_dir + "/.sppserver"

    os.mkdir(main_dir)
    os.mkdir(main_dir + "/Wallets")
    os.mkdir(main_dir + "/Publishes")
    os.mkdir(main_dir + "/Stats")

    api_file = open(main_dir + "/apikey.txt", "w")
    api_file.write(apikey)
    api_file.close()

    pass_file = open(main_dir + "/passphrase.txt", "w")
    pass_file.write(passphrase)
    pass_file.close()

    wallet_list_file = open(main_dir + "/wallets.txt", "w")
    wallet_list_file.close()

    # Here you would populate settings.json with defaults if None and settings specified if some given.

    make_wallet("MainWallet")


# Creates and returns a server_util.Wallet (not a blockchain.wallet.Wallet)
def make_wallet(wallet_name):
    main_dir = os.path.expanduser("~") + "/.sppserver"

    # rewrite with wallets.txt
    if wallet_name in server_util.get_wallet_list() or wallet_name is "":
        print("A wallet with the name " + wallet_name + " already exists.")
        return

    # Create a wallet safely
    try:
        api_code = server_util.get_apikey()
        # print(api_code)
        passphrase = server_util.get_passphrase()
        # print(passphrase)
        wallet = createwallet.create_wallet(password=passphrase, api_code=api_code,
                                            service_url="http://localhost:3000/", label=wallet_name)
        # print(wallet.identifier)
    except APIException as exc:
        print("An error has occurred api side; please try again with make_wallet(" + wallet_name + ").")
        print(exc.args)
        return
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return

    # Makes infrastructure to keep track of wallet in ~/.sppserver
    with open(main_dir + "/wallets.txt", "a") as file:
        file.write(wallet_name + '\n')
        file.close()

    # still have to make [wallet_name].json; the wallet's address folder and things in it (also Wallet object)
    wallet_dct = {"identifier": wallet.identifier, "label": wallet.label, "passphrase": "default"}

    wallet_writer = open(main_dir + "/Wallets/" + wallet_name + ".json", "w")
    wallet_writer.write(json.dumps(wallet_dct, indent=4 * ' '))
    wallet_writer.close()
    # ^only [wallet_name].json

    os.mkdir(main_dir + "/Publishes/" + wallet_name)
    file = open(main_dir + "/Publishes/" + wallet_name + "/tx_hash_list.txt", "w")
    file.close()

    os.mkdir(main_dir + "/Publishes/" + wallet_name + "/Publishmetas")

    return wallet
