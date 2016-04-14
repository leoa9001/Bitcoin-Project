import os
import simplejson as json
import User.user_util as user_util


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
        return "Username already taken"

    home_dir = os.path.expanduser("~")

    with open(home_dir + "/.spp/users.txt", "a") as file:
        file.write(username + '\n')
        file.close()

    # Write in here something to write to usermetas a "[username].json"
    # needs to involve password to generate secretkey publickey pair.
    #
    publickey = user_util.key_gen(password)[1]

    userdict = {"username": username, "publickey": publickey}

    if not description == None:
        userdict["description"] = description

    user_file = open(home_dir + "/.spp/usermetas/" + username + ".json", "w")

    user_file.write(json.dumps(userdict, indent=4 * " "))

    path = home_dir + "/.spp/users"
    os.mkdir(path + "/" + username)
    os.mkdir(path + "/" + username + "/data")
    os.mkdir(path + "/" + username + "/metadata")  # Hash checksums for the data that you push to blockchain

    file = open(path + "/" + username + "/datanames.txt", "w")  # make the file
    file.close()
    file = open(path + "/" + username + "/filenames.txt", "w")
    file.close()
