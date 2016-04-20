import util
from blockchain import blockexplorer
from Server import setup
import blockchain.createwallet
# from User import setup
# from User import user_util
# from User import crypto
import binascii
# wallet = util.get_wallet("MainWallet.json")
# setup.setup()
# setup.create_user("testuser3","testpassword3","Second Test User (with DER)")
# setup.make_wallet("OtherWallet")

l = blockchain.createwallet.create_wallet("password", util.get_apikey(), "http://localhost:3000/")
print("API OUT: "+ util.get_apikey())
print(l.identifier)
# crypto.address(binascii.unhexlify("0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6"))

# user.private_publish("Test file 6", path_to_file= "/Users/leoa9001/Desktop/pdf.pdf", new_file_name="pdh.pdf")

# setup(util.get_apikey(), "TestPassword")


# Should send to: 141sNxH41k4dPPHcDhN8vj8m8K2D8AhWSM from 1JV3cXoFJVNAdtqbXu9ccepS8d5rXBamaH
#
# print(wallet.get_balance())
#
#
# a = wallet.get_address("141sNxH41k4dPPHcDhN8vj8m8K2D8AhWSM")
# print(a.balance)


# transaction = blockexplorer.get_tx(tx_id="fa301b7b12cef049636d348132a375471564cda701b4ef54f1bf6eda4ad9166d")

# print(transaction.block_height)

# for a in transaction.outputs:
#     print(a.address)

# t = wallet.new_address("receive")
# print(t.address)
# file = open("receive.txt","a")
# file.write(t.address)
# file.close()
# for a in wallet.list_addresses():
#     print(a.address)
#
# h = wallet.send("141sNxH41k4dPPHcDhN8vhelloK2D8AhWSM", amount = 5461)


# print(wallet.get_balance())
# print(h.tx_hash)
#
# file = open("tx_hash.txt","a")
# file.write(h.tx_hash)
# file.close()
#
# file = open("rest.txt","w")
# file.write(h.message)
# file.close()
#
# file = open("notice.txt","w")
# file.write(h.notice)
# file.close()

# setup.setup()

# setup.create_user("testuser3","testpassword3", "Third test user")

# user = user_util.get_user("testuser2", "testpassword1")

# user = user_util.get_user("testuser1")
