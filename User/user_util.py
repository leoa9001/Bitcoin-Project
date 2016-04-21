import hashlib
import os
import simplejson as json
from shutil import copyfile
import User.crypto as crypto
import binascii
import Server.server_util


def get_username_list():
    home_dir = os.path.expanduser("~")
    users_file = open(home_dir + "/.spp/users.txt", "r")
    users = []

    for line in users_file:
        if line[line.__len__() - 1] == "\n":
            users.append(line[0:line.__len__() - 1])
        else:
            users.append(line)

    users_file.close()
    return users


# To be written and needs: key_gen and hash and send in



def get_user(username, password=None):
    if password is None:
        return User(username)
    return User(username, password)


# Function that turns arbitrary file into a string; should be updated later.
def to_string(path_to_file):
    file = open(path_to_file, "rb")
    f = file.read()
    file.close()
    return f


# This only works if you have a local working Server of the form outlined in Server and service-my-wallet working
def send_in(address, type="local"):
    # Send in the thing and wait for a response in the form of tx_hash
    if type != "local":
        return "dummytransactionhash"


    tx_hash = Server.server_util.private_publish(address)
    return tx_hash


# Works for constructing users that have already been created using the setup.create_user()
class User:
    __username = None
    __publickey = None
    __privatekey = None
    __description = None

    def __init__(self, username, password=None):
        if (username not in get_username_list()) or ("" == username):
            raise Exception("User with username " + username + " has not been created.")
        self.__username = username

        user_file = open(os.path.expanduser("~") + "/.spp/usermetas/" + username + ".json", "r")
        user_info = json.loads(user_file.read())
        user_file.close()

        if password is None:
            self.__publickey = binascii.unhexlify(user_info["publickey"])
        else:
            keypair = crypto.key_gen(password)
            if binascii.unhexlify(user_info["publickey"]) != keypair[1]:
                # print("userinfo pub: "+user_info["publickey"])
                # print("keypair[1]: "+str(keypair[1]))
                raise Exception("Incorrect password.")
            self.__privatekey = keypair[0]
            self.__publickey = keypair[1]

        if "description" in user_info.keys():
            self.__description = user_info["description"]

    def get_username(self):
        return self.__username

    def get_description(self):
        return self.__description

    def get_publickey(self):
        return self.__publickey

    def get_privatekey(self):
        return self.__privatekey

    def has_description(self):
        return self.__description != None

    def has_privatekey(self):
        return self.__privatekey != None

    def get_datanames_list(self):
        datanames_file = open(os.path.expanduser("~") + "/.spp/users/" + self.__username + "/datanames.txt", "r")
        datanames = []

        for line in datanames_file:
            if line[line.__len__() - 1] == "\n":
                datanames.append(line[0:line.__len__() - 1])
            else:
                datanames.append(line)

        datanames_file.close()
        return datanames

    def get_filenames_list(self):
        filenames_file = open(os.path.expanduser("~") + "/.spp/users/" + self.__username + "/filenames.txt", "r")
        filenames = []

        for line in filenames_file:
            if line[line.__len__() - 1] == "\n":
                filenames.append(line[0:line.__len__() - 1])
            else:
                filenames.append(line)

        filenames_file.close()
        return filenames

    # Returns instance of SPPResponse; only works with text files at the moment
    def private_publish(self, name, path_to_file, new_file_name, description=None):
        if name in User.get_datanames_list(self):
            raise Exception("The name " + name + " is already taken.")
        if new_file_name in User.get_filenames_list(self):
            raise Exception("The filename " + new_file_name + " is already taken.")

        text_data = to_string(path_to_file)
        # print("Text data: ")
        # print(text_data[0:50])
        # print()
        h = hashlib.sha256()
        h.update(self.__publickey)
        h.update(text_data)

        address = crypto.address(h.digest())
        tx_hash = send_in(address)  # may need to check this later.

        dct = {"name": name,
               "filename": new_file_name,
               "hash": str(h.digest(), encoding="utf-8"),
               "address": address,
               "tx_hash": tx_hash
               }
        if description != None:
            dct["description"] = description

        file_path = os.path.expanduser("~") + "/.spp/users/" + self.__username
        metadata_file = open(file_path + "/metadata/unconfirmed/" + name + ".json",
                             "w")

        metadata_file.write(json.dumps(dct, indent=4 * " "))

        copyfile(path_to_file, file_path + "/data/" + new_file_name)

        data_names = open(file_path + "/datanames.txt", "a")
        data_names.write(name + "\n")
        data_names.close()

        file_names = open(file_path + "/filenames.txt", "a")
        file_names.write(new_file_name + "\n")
        file_names.close()
