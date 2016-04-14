# Script to create python wallets (should only be run first)
from blockchain import createwallet
import simplejson as json
import os

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
    file_writer = open("Server/Wallets/" + wall.label + ".json", "w")
    json_encoding = {"identifier": wall.identifier, "address": wall.address, "label": wall.label,
                     "passphrase": "default"}
    json_encoding = json.dumps(json_encoding, indent="    ")
    # print(json_encoding)
    file_writer.writelines(json_encoding)


if os.path.exists("Server/Wallets/MainWallet.json") or os.path.exists("MainWallet.json"):
    print("MainWallet has already been created.")
else:
    main_wallet = createwallet.create_wallet(passphrase,api_code,"http://localhost:3000/",label = "MainWallet")
    file_writer_1 = open("Server/Wallets/MainWallet.json", "w")
    file_writer_2 = open("MainWallet.json","w")
    json_encoding = {"identifier": wall.identifier, "address": wall.address, "label": wall.label,
                     "passphrase": "default"}
    json_encoding = json.dumps(json_encoding, indent="    ")
    # print(json_encoding)
    file_writer_1.writelines(json_encoding)
    file_writer_2.writelines(json_encoding)

