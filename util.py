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




