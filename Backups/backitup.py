import datetime
import os
import shutil


def backitup(path_to_dir, description=None):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)

    now = datetime.datetime.now()
    timestamp = str(int(now.timestamp()))

    os.mkdir(path_to_dir + "/" + timestamp)

    shutil.copytree(os.path.expanduser("~") + "/.spp", path_to_dir + "/" + timestamp + "/spp")
    shutil.copytree(os.path.expanduser("~") + "/.sppserver", path_to_dir + "/" + timestamp + "/sppserver")
    file = open(path_to_dir + "/" + timestamp + "/date.txt", "w")
    file.write(str(now))
    file.close()

    print("Successfully backed up spp and sppserver on " + timestamp)

    if description is not None:
        file = open(path_to_dir + "/" + timestamp + "/description.txt", "w")
        file.write(description)
        file.close()


def rebase(backup_dir, timestamp):
    home = os.path.expanduser("~")

    main_dir = backup_dir +"/"+timestamp

    if not os.path.exists(main_dir):
        raise Exception("Invalid Backup folder.")
        return

    if os.path.exists(home+"/.spp"):
        shutil.rmtree(home+"/.spp")
    if os.path.exists(home+"/.sppserver"):
        shutil.rmtree(home+"/.sppserver")

    shutil.copytree(main_dir+"/spp", home+"/.spp")
    shutil.copytree(main_dir+"/sppserver", home+"/.sppserver")

