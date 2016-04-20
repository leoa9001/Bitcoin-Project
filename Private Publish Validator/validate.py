from blockchain import blockexplorer
from blockchain.util import APIException

def validate(tx_hash, address):
    try:
        tx = blockexplorer.get_tx(tx_hash, api_code = get_apikey())
    except APIException:
        print("An exception occurred api side. The transaction may not have gone in.")
    except:
        print("An unexpected error occurred.")

    for a in tx.outputs:
        if a.address==address:
            print("Address match: "+address)
        print("Address Mismatch: "+a.address)

    return (tx.outputs,tx.time,tx.block_height)



def get_apikey():
    file = open("Private Publish Validator/apikey.txt", "r")
    api_code = file.read()
    file.close()
    return api_code

