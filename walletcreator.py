# Script to create python wallets (should only be run first)
from blockchain import createwallet
import simplejson as json

file = open("apikey.txt", "r")
api_code = file.read()
file.close()

passfile = open("password.txt", "r")
passphrase = passfile.read()
passfile.close()

testwallet = createwallet.create_wallet(passphrase, api_code, "http://localhost:3000/", label="TestWallet")

wallets = [testwallet]

wallets.append(createwallet.create_wallet(passphrase, api_code, "http://localhost:3000/", label="Wallet1"))
wallets.append(createwallet.create_wallet(passphrase, api_code, "http://localhost:3000/", label="Wallet2"))
wallets.append(createwallet.create_wallet(passphrase, api_code, "http://localhost:3000/", label="DonationWallet"))

for wall in wallets:
    file_writer = open("Wallets/" + wall.label + ".json", "w")
    json_encoding = {"identifier": wall.identifier, "address": wall.address, "label": wall.label,
                     "passphrase": "default"}
    json_encoding = json.dumps(json_encoding, indent="    ")
    # print(json_encoding)
    file_writer.writelines(json_encoding)
