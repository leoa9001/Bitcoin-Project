

from blockchain import createwallet
import util


passfile = open("password.txt", "r")
passphrase = passfile.read()
passfile.close()


testwallet = util.get_wallet("testwallet.txt")




def create_test_wallet(label, passphrase = None):
    if passphrase is None:
        pass_file = open("password.txt")
        passphrase = pass_file.read()

    return createwallet.create_wallet(passphrase,api_code,'http://localhost:3000/',label = label)

#Script 2: getting a wallet and outputting it's label and it's balance
#
# wallet = util.get_wallet("testwallet.txt")
#
# addresses = wallet.list_addresses()
#
# for a in addresses:
#     print(a.get_balance())
#
# util.print_the_thing()

