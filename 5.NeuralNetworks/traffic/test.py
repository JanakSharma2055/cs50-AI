import os

for root, dir, files in os.walk("gtsrb-small"):
        for file_name in files:
            #reads each image as an array of rgb
            print(file_name)
