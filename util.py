from blockchain.wallet import Wallet
import simplejson as json
import datetime

#easier way to get the apikey
def get_apikey():
    file = open("apikey.txt","r")
    apikey = file.read()
    file.close()
    return apikey

def get_passphrase():
    file = open("password.txt", "r")
    passphrase = file.read()
    file.close()
    return passphrase

#easy way to get a wallet via
def get_wallet(filename,passphrase = None):
    if passphrase is None:
        passfile = open("password.txt","r")
        passphrase = passfile.read()
        passfile.close()

    file = open(filename,"r")
    identifier = json.loads(file.read()).get("identifier")
    return Wallet(identifier, passphrase, "http://localhost:3000/",api_code=get_apikey())

# Return current time as an integer
def get_current_time():
    return int(datetime.datetime.now().timestamp())






