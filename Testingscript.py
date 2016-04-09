import User.user_util as user_util
# import shutil

# from blockchain import createwallet
# import util
# import simplejson as json
#
#
# passfile = open("password.txt", "r")
# passphrase = passfile.read()
# passfile.close()
#
#
# testwallet = util.get_wallet("Wallets/TestWallet.json")
#
# file1 = open("/Users/leoa9001/Desktop/Dox.png","rb")
#
# file2 = open("/Users/leoa9001/Desktop/tmp/Dox.png","rb")
#
# shutil.copyfile("/Users/leoa9001/Desktop/Dox.png", "/Users/leoa9001/Desktop/GearTesting/Tox.png")
#
# print(file1.read()==file2.read())
#
#
# file1.close()
# file2.close()

user = user_util.get_user("testuser1")

user.private_publish("Doxitius Picture", "/Users/leoa9001/Desktop/Dox.png", "Tox.png", description = "A picture of a friend whose ign is Toxidius")

