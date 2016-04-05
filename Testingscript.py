

from blockchain import createwallet

file = open("apikey.txt", "r")
api_code = file.read()
file.close()

pass_file = open("password.txt", "r")
passphrase = pass_file.read()
pass_file.close()


testwallet = createwallet.create_wallet(passphrase, api_code, "http://localhost:3000/", label = "Test Wallet")

testwallet_file_writer = open("testwallet.txt","w")

testwallet_file_writer.write(testwallet.identifier)
testwallet_file_writer.write("\n")
testwallet_file_writer.write(testwallet.address)
testwallet_file_writer.write('\n')
testwallet_file_writer.write(testwallet.label)


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