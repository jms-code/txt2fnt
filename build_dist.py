import os
import shutil


distFolder = "dist"
# check if distFolder exists, if not create it
if not os.path.exists(distFolder):
    os.makedirs(distFolder)
else:
    # clean up existing files in distFolder deeply
    for root, dirs, files in os.walk(distFolder):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))


folders = ["_tools_", "config"]
