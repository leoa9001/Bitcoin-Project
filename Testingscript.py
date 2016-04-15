# import util
# from blockchain import blockexplorer

from User import setup
from User import user_util

# wallet = util.get_wallet("MainWallet.json")

# Should send to: 141sNxH41k4dPPHcDhN8vj8m8K2D8AhWSM from 1JV3cXoFJVNAdtqbXu9ccepS8d5rXBamaH
#
# print(wallet.get_balance())
#
#
# a = wallet.get_address("1MkqaB4cYCtVJ31fgyifdJ4CbgSuf69yvf")
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
# h = wallet.send("1MkqaB4cYCtVJ31fhelloJ4CbgSuf69yvf",amount = 5461)
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

setup.create_user("testuser2","testpassword2", "Second test user")

# user = user_util.get_user("testuser2", "testpassword1")

# user = user_util.get_user("testuser1")


