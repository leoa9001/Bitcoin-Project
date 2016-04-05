from blockchain.wallet import Wallet


#easier way to get the apikey
def get_apikey():
    file = open("apikey.txt","r")
    apikey = file.read()
    file.close()
    return apikey

#easy way to get a wallet via
def get_wallet(filename,passphrase = None):
    if passphrase is None:
        passfile = open("password.txt","r")
        passphrase = passfile.read()
        passfile.close()

    file = open(filename,"r")
    identifier = file.readline()
    print("Identifier to loaded wallet: "+identifier)
    return Wallet(identifier, passphrase, "http://localhost:3000")


def print_the_thing():
    print("DO THE THING!")


wallet = get_wallet("testwallet.txt")

print(wallet.get_address("1HjjjnnPuLz3WCkkx69P1q8CjwP9rjwur").label)



