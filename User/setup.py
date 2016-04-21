import os
import simplejson as json
import User.user_util as user_util
import User.crypto as crypto
import binascii


def setup():
    home_dir = os.path.expanduser("~")
    if os.path.exists(home_dir + "/.spp"):
        print("SPP Folder has already been made.")
        return

    os.mkdir(home_dir + "/.spp")
    os.mkdir(home_dir + "/.spp/users")
    os.mkdir(home_dir + "/.spp/usermetas")
    file = open(home_dir + "/.spp/users.txt", "w")
    file.close()
    # print("Full run.")


# Returns a response message.

def create_user(username, password, description=None):
    if username in user_util.get_username_list():
        print("Username already taken.")
        return "Username already taken"

    home_dir = os.path.expanduser("~")

    with open(home_dir + "/.spp/users.txt", "a") as file:
        file.write(username + '\n')
        file.close()

    # Write in here something to write to usermetas a "[username].json"
    # needs to involve password to generate secretkey publickey pair.
    #
    public_key = binascii.hexlify(crypto.key_gen(password)[1])

    user_dict = {"username": username, "publickey": public_key}

    if description is not None:
        user_dict["description"] = description

    user_file = open(home_dir + "/.spp/usermetas/" + username + ".json", "w")

    user_file.write(json.dumps(user_dict, indent=4 * " "))

    path = home_dir + "/.spp/users"
    os.mkdir(path + "/" + username)
    os.mkdir(path + "/" + username + "/data")
    os.mkdir(path + "/" + username + "/metadata")  # Hash checksums for the data that you push to blockchain
    os.mkdir(path + "/" + username + "/metadata/unconfirmed")
    os.mkdir(path + "/" + username + "metadata/confirmed")

    file = open(path + "/" + username + "/datanames.txt", "w")  # make the file
    file.close()
    file = open(path + "/" + username + "/filenames.txt", "w")
    file.close()
