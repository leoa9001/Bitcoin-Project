import hashlib
import os
import simplejson as json
from shutil import copyfile
from shutil import copytree
import User.crypto as crypto
import binascii
import Server.server_util
import datetime
import Verifier.verify as verify


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


def get_user(username, password=None):
    if password is None:
        return User(username)
    return User(username, password)


# Function that turns arbitrary file/directory into a bytearray.
def to_bytes(path_to_file):
    if os.path.isfile(path_to_file):
        file = open(path_to_file, "rb")
        f = file.read()
        file.close()
        return f

    if os.path.isdir(path_to_file):
        byte_array = bytearray()
        for root, dirs, files in os.walk(path_to_file):
            for file in files:
                file = open(root+"/"+file,"rb")
                byte_array+=file.read()
                file.close()
        return bytes(byte_array)
    return b""

# This only works if you have a local working Server of the form outlined in Server and service-my-wallet working
def send_in(hash, type="local"):
    # Send in the thing and wait for a response in the form of tx_hash
    if type != "local":
        return "dummytransactionhash"


    address = crypto.address(hash)

    tx_hash = Server.server_util.private_publish(hash, address)
    return tx_hash


# Return current time as an integer
def get_current_time():
    return int(datetime.datetime.now().timestamp())


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
        return self.__description is not None

    def has_privatekey(self):
        return self.__privatekey is not None

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
    def private_publish(self, name, path_to_data, new_data_name, description=None):
        if name in User.get_datanames_list(self):
            raise Exception("The name " + name + " is already taken.")
        if new_data_name in User.get_filenames_list(self):
            raise Exception("The filename " + new_data_name + " is already taken.")

        text_data = to_bytes(path_to_data)
        h = hashlib.sha256()
        h.update(self.__publickey)
        h.update(text_data)


        tx_hash = send_in(h.digest())  # may need to check this later.

        if tx_hash == "failed private publish":
            raise Exception("Private publish failed server side.")
            return

        dct = {
            "name": name,
            "filename": new_data_name,
            "hash": h.hexdigest(),
            "address": crypto.address(h.digest()),
            "tx_hash": tx_hash,
            "time": get_current_time()
        }

        if description != None:
            dct["description"] = description

        file_path = os.path.expanduser("~") + "/.spp/users/" + self.__username

        if os.path.isfile(path_to_data):
            copyfile(path_to_data, file_path + "/data/" + new_data_name)
        elif os.path.isdir(path_to_data):
            copytree(path_to_data, file_path + "/data/" + new_data_name)
        else:
            raise Exception("Error in copying file.")


        metadata_file = open(file_path + "/metadata/unconfirmed/" + name + ".json", "w")

        metadata_file.write(json.dumps(dct, indent=4 * " "))

        data_names = open(file_path + "/datanames.txt", "a")
        data_names.write(name + "\n")
        data_names.close()

        file_names = open(file_path + "/filenames.txt", "a")
        file_names.write(new_data_name + "\n")
        file_names.close()

    def validate(self, dataname=None):
        if dataname is None:
            path = os.path.expanduser("~") + "/.spp/users/" + self.__username + "/metadata"
            for filename in os.listdir(path=path + "/unconfirmed"):
                if filename.endswith(".json"):
                    file = open(path + "/unconfirmed/" + filename, "r")
                    dct = json.loads(file.read())
                    file.close()
                    try:
                        response = verify.verify(dct["tx_hash"], dct["address"])
                    except Exception as e:
                        print("Verification Exception:")
                        print(e.args)
                        continue

                    if response[1] == -1:
                        print("Unconfirmed file " + filename + ". However, the tx has gone in and should be confirmed soon.")
                        continue

                    dct["realtime"] = response[0]
                    dct["timedifference"] = response[0] - int(dct["time"])

                    file = open(path + "/confirmed/" + filename, "w")
                    file.write(json.dumps(dct, indent=4 * ' '))
                    file.close()

                    os.remove(path=path + "/unconfirmed/" + filename)

                    print("Validated file: " + filename + ".")

    def check_corruptions(self, safe_print=False):
        try:
            self.validate()
        except Exception as e:
            print("Error occurred in validation.")
            print(e.args)
            return False
        path = os.path.expanduser("~") + "/.spp/users/" + self.__username + "/metadata/confirmed"

        list_of_corrupted = []
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                corrupted = False

                try:
                    file = open(path + "/" + filename, "r")
                    dct = json.loads(file.read())
                    file.close()

                    path_to_data = os.path.expanduser("~") + "/.spp/users/" + self.__username + "/data/" + dct[
                        "filename"]

                    text_data = to_bytes(path_to_data)
                except:
                    print("An error occurred in file handling on file: " + filename)
                    print("Some files may be missing or the filename may be corrupted.")
                    list_of_corrupted.append(filename)
                    continue

                h = hashlib.sha256()
                h.update(self.__publickey)
                h.update(text_data)

                if not h.hexdigest() == dct["hash"]:
                    print("Hash mismatch error on file: " + filename)
                    corrupted = True
                if not crypto.address(h.digest()):
                    print("Address mismatch error on file: " + filename)
                    corrupted = True

                if corrupted:
                    list_of_corrupted.append(filename)
                elif safe_print:
                    print("The file " + filename + " is not corrupted.")

        if list_of_corrupted.__len__() > 0:
            print("THE FOLLOWING DATA ARE CORRUPTED IN SOME WAY:")

        for dataname in list_of_corrupted:
            print(dataname + "is corrupted.")
