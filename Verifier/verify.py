from blockchain import blockexplorer
from blockchain.util import APIException


def verify(tx_hash, address):
    try:
        tx = blockexplorer.get_tx(tx_hash, api_code=get_apikey())
    except APIException:
        print("An exception occurred api side. The transaction may not have gone in.")
        return
    except:
        print("An unexpected error occurred.")
        return

    match = False
    for a in tx.outputs:
        if a.address == address:
            match = True
            break

    if not match:
        raise Exception("Transaction address may not have matched")

    return (tx.time, tx.block_height)


def get_apikey():
    file = open("Verifier/apikey.txt", "r")
    api_code = file.read()
    file.close()
    return api_code
