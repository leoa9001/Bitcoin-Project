import datetime
import os
import shutil




def backitup(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)

    now = datetime.datetime.now()
    timestamp = str(int(now.timestamp()))

    os.mkdir(path_to_dir+"/"+timestamp)

    shutil.copytree(os.path.expanduser("~")+"/.spp", path_to_dir+"/"+timestamp+"/spp")
    shutil.copytree(os.path.expanduser("~")+"/.sppserver", path_to_dir+"/"+timestamp+"/sppserver")
    file = open(path_to_dir+"/"+timestamp+"/date.txt", "w")
    # print(now)
    file.write(str(now))
    file.close()

    print("Successfully backed up spp and sppserver on "+ timestamp)