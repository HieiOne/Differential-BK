#!/usr/bin/env python3
#TODO configuration file apart, pretty GUI
import os, hashlib, json
from shutil import copy2

###WINDOWS###
backup_folder = {1: "D:\projects\own-differential-backup\\backup"} #Just add 2: "Path", for new syncs
data_folder = {1: "D:\projects\own-differential-backup\data"}
file_snapshot_location = {1: "D:\projects\own-differential-backup\data_file.json"}
folder_snapshot_location = {1: "D:\projects\own-differential-backup\data_folder.json"}

###LINUX####
#data_folder = {1: "/mnt/SHARED_DATA/Repository/odb/data"}
#backup_folder = {1: "/mnt/SHARED_DATA/Repository/odb/backup"}
#file_snapshot_location = {1: "/mnt/SHARED_DATA/Repository/odb/data_file.json"}
#folder_snapshot_location = {1: "/mnt/SHARED_DATA/Repository/odb/data_folder.json"}

def create_json(f_json, data): #data = {} or [] depending if its list or dictionary
    f = open(f_json,"w+")
    f.write(data)
    f.close()

def save_data(snapshot_location, data):
    with open(snapshot_location, 'w') as fp:
        json.dump(data, fp)

def load_data(snapshot_location):
    with open(snapshot_location, 'r') as fp:
        data = json.load(fp)
    return data

def hash(file): #defines md5sum of passed files
    return hashlib.md5(open(file,'rb').read(4096)).hexdigest() # the 4096 is to allow big files

def make_dirs(directory, folders_snapshot, data_folder, backup_folder): #make folders
    _directory = directory.replace(data_folder, backup_folder) #decode to remove the bytes b'' of python
    os.makedirs(_directory, exist_ok=True) #exist_ok allows me to avoid folders which already exists
    folders_snapshot.append(os.path.join(directory))

def remove_dirs(directory, data_directory, folders_snapshot): #remove folders (Not implemented)
    print(data_directory, "Folder was not found, removing...")
    os.removedirs(directory)
    folders_snapshot.remove(data_directory) #works, I don't use del because it breaks with empty folders

def remove_files(file, data_file, files_snapshot): #remove files (Not implemented)
    print(data_file, "Was not found, removing...")
    os.remove(file)
    del files_snapshot[data_file]

def copy_file(file, md5, files_snapshot, data_folder, backup_folder): #copy files
    print("Copying file", file)
    destination = file.replace(data_folder, backup_folder) #destination -> backup path, file -> data path
    copy2(file, destination)
    files_snapshot[file] = md5 #this subs the key also

def look_for_new_files(data_folder, backup_folder, files_snapshot, folders_snapshot): #this is to find new files and folders to add 
    for subdir, dirs, files in os.walk(data_folder): #os.walk returns 3 values, subdirs, dirs and files
        if not dirs and not files: #detects empty sub-folders
            make_dirs(subdir, folders_snapshot, data_folder, backup_folder)

        for file in files:
            file = os.path.join(subdir,file) #putting path and file name together
            _file = os.path.join(subdir,file)
            md5 = hash(file) #calculating the md5sum

            if subdir not in folders_snapshot:
                make_dirs(subdir, folders_snapshot, data_folder, backup_folder) #subdirs lets me grab only the directories :thumbs_up:

            if (_file not in files_snapshot) or (files_snapshot[_file] != md5): #no need to re-add, going to implement a checking function (BUG: check subdir+file, not only file)
                copy_file(file, md5, files_snapshot, data_folder, backup_folder)

def look_for_removen_files(backup_folder, data_folder, files_snapshot, folders_snapshot): #this is to find removen files and folders to remove from backup folder
    for subdir, dirs, files in os.walk(backup_folder):
        folder = subdir
        _folder = subdir.replace(backup_folder, data_folder) #to check if it's on data folder

        if not dirs and not files and not os.path.exists(_folder): #removes empty folders
            remove_dirs(folder, _folder, folders_snapshot)

        for file in files: #gotta remove file not data_file, remember you cunt
            file = os.path.join(subdir, file)
            _file = file
            data_file = file.replace(backup_folder, data_folder)

            if not os.path.exists(data_file):
                remove_files(_file, data_file, files_snapshot)
            
            if not os.path.exists(_folder): #works but can't remove not empty folders
                remove_dirs(folder, _folder, folders_snapshot)

def main(data_folder, backup_folder, file_snapshot_location, folder_snapshot_location):
    if not os.path.exists(file_snapshot_location) or not os.path.exists(folder_snapshot_location): #checks if the .json exists and if not it creates them
        create_json(file_snapshot_location, "{}")
        create_json(folder_snapshot_location, "[]")
    files_snapshot = load_data(file_snapshot_location) #only files
    folders_snapshot = load_data(folder_snapshot_location) #only folders
    look_for_new_files(data_folder, backup_folder, files_snapshot, folders_snapshot)
    look_for_removen_files(backup_folder, data_folder, files_snapshot, folders_snapshot)
    save_data(file_snapshot_location, files_snapshot) #saves the new file_snapshot
    save_data(folder_snapshot_location, folders_snapshot) #saves the new folder_snapshot

#it all starts here

if __name__ == "__main__":
    for key in backup_folder: #anyway I don't need to count keys if every list should have the same ones
        main(data_folder[key], backup_folder[key], file_snapshot_location[key], folder_snapshot_location[key])