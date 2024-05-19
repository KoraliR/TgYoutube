import os
way = os.getcwd()
name = "\\PATH_TO_DOWNLOAD.txt"
with open(way + name, "r") as file:
    for i in file:
        PATH = i
print(PATH)


