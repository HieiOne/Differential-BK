#!/usr/bin/env python3
#TODO remove folders function, if .json doesn't exist: create it, define what i can define in the functions and clear out the for's
#Known bugs: Doesn't detect empty folders

import os, hashlib, json
from shutil import copy2

backup_folder = os.fsencode("D:\projects\own-differential-backup\\backup")
data_folder = os.fsencode("D:\projects\own-differential-backup\data")
file_snapshot_location = os.fsencode("D:\projects\own-differential-backup\data_file.json")
folder_snapshot_location = os.fsencode("D:\projects\own-differential-backup\data_folder.json")

def make_dirs(directory): #make folders
    directory = directory.replace(data_folder, backup_folder).decode('utf-8') #decode to remove the bytes b'' of python
    os.makedirs(directory, exist_ok=True) #exist_ok allows me to avoid folders which already exists

def remove_dirs(directory): #remove folders (Not implemented)
    os.removedirs(directory)

def remove_files(file): #remove files (Not implemented)
    os.remove(file)

def copy_file(file): #copy files
    destination = file.replace(data_folder, backup_folder).decode('utf-8') #destination -> backup path, file -> data path
    copy2(file, destination)

def hash(file): #defines md5sum of passed files
    return hashlib.md5(open(file,'rb').read(4096)).hexdigest() # the 4096 is to allow big files

def save_data(snapshot_location, data):
    with open(snapshot_location, 'w') as fp:
        json.dump(data, fp)

def load_data(snapshot_location):
    with open(snapshot_location, 'r') as fp:
        data = json.load(fp)
    return data

#it all starts here

files_snapshot = load_data(file_snapshot_location) #only files
folders_snapshot = load_data(folder_snapshot_location) #only folders

#this is to add new files and folders
for subdir, dirs, files in os.walk(data_folder):
    for file in files:
        file = os.path.join(subdir,file) #putting path and file name together
        _file = os.path.join(subdir,file).decode('utf-8')
        md5 = hash(file) #calculating the md5sum

        if subdir not in folders_snapshot:
            make_dirs(subdir) #subdirs lets me grab only the directories :thumbs_up:
            folders_snapshot.append(os.path.join(subdir.decode('utf-8')))

        if (_file not in files_snapshot) or (files_snapshot[_file] != md5): #no need to re-add, going to implement a checking function (BUG: check subdir+file, not only file)
            print("Copying file", _file)
            copy_file(file)
            files_snapshot[file.decode('utf-8')] = md5 #this subs the key also
        else:
            pass

#this is to remove file's and folder's which aren't in data_folder anymore
for subdir, dirs, files in os.walk(backup_folder):
    for file in files: #gotta remove file not data_file, remember you cunt
        file = os.path.join(subdir, file)
        _file = file.decode('utf-8')
        data_file = file.replace(backup_folder, data_folder).decode('utf-8')
        
        if subdir not in folders_snapshot:
            pass

        if not os.path.exists(data_file):
            print(data_file, "Was not found")
            os.remove(_file)
            del files_snapshot[data_file] #add an execption that in case i couldn't remove it from the files_snapshot, to remove the file eitherway without giving a KeyError



save_data(file_snapshot_location, files_snapshot) #saves the new file_snapshot
save_data(folder_snapshot_location, folders_snapshot) #saves the new folder_snapshot
