import hashlib
import os
import simplejson as json
from shutil import copyfile


def get_username_list():
    home_dir = os.path.expanduser("~")
    users_file = open(home_dir + "/.spp/users.txt", "r")
    users = []

    for line in users_file:
        if line[line.__len__() - 1] == "\n":
            users.append(line[0:line.__len__() - 1])
        else:
            users.append(line)

    return users


# To be written and needs: key_gen and hash and send in

# Temporary keygen until can come up with safe asymmetric encryption generated by passphrase
def key_gen(passphrase):
    # Make objects privatekey and publickey and return them as a tuple
    return ("dummyprivatekey", "dummypublickey")


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


def send_in(User, hash):
    # Send in the thing and wait for a response in the form of tx_hash

    # For Now:
    return "dummytransactionhash"


# Works for constructing users that have already been created using the setup.create_user()
class User:
    __username = None
    __publickey = None
    __privatekey = None
    __description = None

    def __init__(self, username, password=None):
        if (username not in get_username_list()) and (username != ""):
            raise Exception("User with username " + username + " has not been created.")
        self.__username = username

        user_file = open(os.path.expanduser("~") + "/.spp/usermetas/" + username + ".json", "r")
        user_info = json.loads(user_file.read())
        user_file.close()

        if password is None:
            self.__publickey = user_info["publickey"]
        else:
            keypair = key_gen(password)
            if user_info["publickey"] != keypair[1]:
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

    # Returns instance of SPPResponse; only works with text files at the moment
    def private_publish(self, name, path_to_file, new_file_name, description=None):
        text_data = to_string(path_to_file)
        h = hashlib.sha256()
        h.update((self.__publickey).encode("utf-8"))
        h.update(str(text_data).encode("utf-8"))
        tx_hash_digest = send_in(self, h)

        hash = hashlib.sha256()
        hash.update(str(text_data).encode("utf-8"))

        dct = {"name": name}
        dct["filename"] = new_file_name
        dct["hash"] = hash.hexdigest()
        dct["tx_hash"] = tx_hash_digest
        if description != None:
            dct["description"] = description

        file_path = os.path.expanduser("~")+"/.spp/users/"+self.__username
        metadata_file = open(file_path + "/metadata/" + name + ".json",
                             "w")

        metadata_file.write(json.dumps(dct, indent=4 * " "))

        copyfile(path_to_file, file_path + "/data/" + new_file_name)

        datanames = open(file_path+"/datanames.txt", "a")

        datanames.write(name+"\n")

        datanames.close()
