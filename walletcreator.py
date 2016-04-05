#Script to create python wallets (should only be run first)
from blockchain.wallet import Wallet
from blockchain import createwallet

file = open("apikey.txt", "r")
api_code = file.read()
file.close()

passfile = open("password.txt", "r")
passphrase = passfile.read()
passfile.close()


testwallet = createwallet.create_wallet(passphrase, api_code,"http://localhost:3000/",label = "Test Wallet")




