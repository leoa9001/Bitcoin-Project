import os


def get_apikey():
    file = open(os.path.expanduser("~")+"/.sppserver/apikey.txt","r")
    apikey = file.read()
    file.close()
    return apikey

def get_passphrase():
    file = open(os.path.expanduser("~")+"/.sppserver/passphrase.txt", "r")
    passphrase = file.read()
    file.close()
    return passphrase


# Gets list of wallets (wallets made via create_wallet and definitely does not include Store wallet)
def get_wallet_list():
    wallets_file = open(os.path.expanduser("~")+"/.sppserver/wallets.txt", "r")
    wallets = []

    for line in wallets_file:
        if line[line.__len__()-1] == "\n":
            wallets.append(line[0:line.__len__()-1])
        else:
            wallets.append(line)

    wallets_file.close()
    return wallets


