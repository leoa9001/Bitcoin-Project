#Script to create python wallets (should only be run first)


file = open("apikey.txt","r")
api_code = file.read()
file.close()

passfile = open("Password.txt","r")
passphrase = passfile.read()
passfile.close()

