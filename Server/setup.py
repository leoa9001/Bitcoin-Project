import os
from blockchain.exceptions import APIException
from blockchain.createwallet import create_wallet
import sys
from Server import server_util
import simplejson as json





# Sets main folder and such
def setup(apikey, passphrase, settings=None):
    home_dir = os.path.expanduser("~")
    if os.path.exists(home_dir + "/.sppserver"):
        print("SPP Server has already been set up.")
        return

    os.mkdir(home_dir + "/.sppserver")
    os.mkdir(home_dir + "/.sppserver/Wallets")
    os.mkdir(home_dir + "/.sppserver/Addresses")

    api_file = open(home_dir + "/.sppserver/apikey.txt", "w")
    api_file.write(apikey)
    api_file.close()

    pass_file = open(home_dir + "/.sppserver/passphrase.txt", "w")
    pass_file.write(passphrase)
    pass_file.close()

    wallet_list_file = open(home_dir + "/.sppserver/wallets.txt", "w")
    wallet_list_file.close()


    # Here you would populate settings.json with defaults if None and settings specified if some given.


    # Here you would make the store wallet using functions from store_wallet.py


    # Here you would call function create_wallet("MainWallet") from server_util.py


# Creates and returns a server_util.Wallet (not a blockchain.wallet.Wallet)
def create_wallet(wallet_name):
    main_dir = os.path.expanduser("~") + "/.sppserver"
    if os.path.exists(main_dir + "/Addresses/" + wallet_name):
        print("A wallet with the name " + wallet_name + " already exists.")
        return

    # Create a swallet safely
    try:
        api_code = server_util.get_apikey()
        passphrase = server_util.get_passphrase()
        wallet = create_wallet(passphrase, api_code, "http://localhost:3000/", wallet_name)
    except APIException as exc:
        print("An error has occurred api side; please try again with createwallet(" + wallet_name + ").")
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
    os.mkdir(main_dir + "/Addresses/" + wallet_name)

    return wallet
