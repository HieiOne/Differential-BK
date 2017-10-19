#!/usr/bin/env python3
#TODO Checking function(could implement an OR in the first for), remove files function, remove folders function
#Known bugs: Doesn't detect empty folders

import os, hashlib, json
from shutil import copy2

backup_folder = os.fsencode("D:\projects\own-differential-backup\\backup")
data_folder = os.fsencode("D:\projects\own-differential-backup\data")
snapshot_location = os.fsencode("D:\projects\own-differential-backup")

files_snapshot = {} #only files
folders_snapshot = [] #only folders

def make_dirs(directory): #make folders
    directory = directory.replace(data_folder, backup_folder).decode('utf-8') #decode to remove the bytes b'' of python
    os.makedirs(directory, exist_ok=True) #exist_ok allows me to avoid folders which already exists

def remove_dirs(directory): #remove folders (Not implemented)
    pass

def remove_files(file): #remove files (Not implemented)
    pass

def check_file(file): #copy files
    destination = file.replace(data_folder, backup_folder).decode('utf-8') #destination -> backup path, file -> data path
    copy2(file, destination)

def hash(file): #defines md5sum of passed files
    return hashlib.md5(open(file,'rb').read(4096)).hexdigest() # the 4096 is to allow big files

def save_data(dictionary):
    with open('data.json', 'w') as fp:
    json.dump(data, fp)
    

for subdir, dirs, files in os.walk(data_folder):
    for file in files:
        file = os.path.join(subdir,file) #putting path and file name together
        md5 = hash(file) #calculating the md5sum

        if subdir not in folders_snapshot:
            make_dirs(subdir) #subdirs lets me grab only the directories :thumbs_up:
            folders_snapshot.append(os.path.join(subdir.decode('utf-8')))

        if file not in files_snapshot: #no need to re-add, going to implement a checking function (BUG: check subdir+file, not only file)
            check_file(file)
            files_snapshot[file] = md5
        else:
            print("everything seems fine")


print(files_snapshot)
