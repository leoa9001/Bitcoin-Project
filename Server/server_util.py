import os
import simplejson as json
from blockchain import wallet

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



#Server utilities

#Main Wallet by default
def get_wallet(wallet_name = "MainWallet"):
    wallet_file = open(os.path.expanduser("~")+"/.sppserver/Wallets/"+wallet_name+".json")
    wallet_json = json.loads(wallet_file.read())
    wallet_file.close()

    if wallet_json["passphrase"] is "default":
        passphrase = get_passphrase()
    else:
        passphrase = wallet_json["passphrase"]


    return wallet.Wallet(identifier = wallet_json["identifier"], password = passphrase, service_url="http://localhost:3000/", api_code= get_apikey())


#Should return the transaction hash:
def private_publish(address, wallet_name = "MainWallet"):
    wallet = get_wallet(wallet_name)

    response = wallet.send(to = address, amount = 5461)


    #Write in data here
    file = open(os.expanduser("~")+ "/.sppserver/Publishes/"+wallet_name+"/tx_hash_list.txt", "a")
    file.write(response.tx_hash+"\n")
    file.close()

    return response.tx_hash