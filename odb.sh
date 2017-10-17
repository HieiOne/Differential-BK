#!/bin/bash
#TODO implement a function which will actually remove the moved folders and files after "x" time
export backup_directory="/mnt/SHARED_DATA/Repository/backup/oib/backup"
export directory="/mnt/SHARED_DATA/Repository/backup/oib/test"
export snapshot_file="$backup_directory/.snapshot.md5" #creating file with known files 
export backup_structure="$backup_directory/backup-folder-structure.temp" #this is to be able to remove folders
export temporary_folder="$backup_directory/LOST+FOUND"
export time_of_life="7"

function snapshot(){ #$1 = File location
  echo "CREATING NEW REGISTER: $1...       [OK]"
  md5sum "$1" >> "$snapshot_file"
}

function checking(){ #$1 = File location
  md5temp=$(md5sum "$1" | cut -d" " -f1)
  md5=$(cat "$snapshot_file" | grep -w "$1" | cut -d" " -f1)
  newpath="${1/$directory/$backup_directory}" #transforming the path

  if [[ "$md5" == "$md5temp" ]]; then #FILE is found and not modified in tree
    echo -n "" #will change this in future
  elif ! grep -w "$1" "$snapshot_file"; then #FILE is not FOUND in snapshot
    echo "NEW REGISTER: ADDING $1 TO THE REGISTER"
    md5sum "$1" >> "$snapshot_file"
    cp -R "$1" "$newpath"
  else
    echo "REGISTER: $1           [MODIFIED]" #FILE is found but modified in tree
    newreg=$(md5sum "$1")
    sed -i "s|.*$1|$newreg|g" "$snapshot_file" 2> /dev/null
    cp -R "$1" "$newpath"
  fi
}

function createfolders(){
  newpath="${1/$directory/$backup_directory}" #transforming the path
  mkdir -p "$newpath"
  mkdir -p "$temporary_folder"
}

function moving_files(){
  while read line; do
    c_file=$(echo $line | cut -d" " -f2)
    if [ ! -f "$c_file" ]; then
      echo "$c_file Doesn't exist [REMOVING]"
      sed -i "s|.*$c_file||" "$snapshot_file" 2> /dev/null ; sed -i "/^$/d" "$snapshot_file" 2> /dev/null
      d_file="${c_file/$directory/$backup_directory}"
      mv "$d_file" "$temporary_folder"
    fi
  done < $snapshot_file
}

function moving_folders(){
  find "$backup_directory" -type d > $backup_structure
  while read line; do
    c_folder=$(echo $line)
    d_folder="${c_folder/$backup_directory/$directory}"
    if [ ! -d "$d_folder" ] && [[ "$c_folder" != $temporary_folder* ]];then #so it wont interfere in the last found directory
      echo "$d_folder Doesn't exist [REMOVING]"
      mv "$c_folder" "$temporary_folder"
    fi
  done < $backup_structure
  rm $backup_structure
}

export -f checking
export -f snapshot
export -f createfolders

#generating first snapshot file in case it doesn't exist
if [ ! -f "$snapshot_file" ]; then
  touch "$snapshot_file"
  echo "CREATING NEW SNAPSHOT FILE"
  find "$directory" -type f -exec bash -c 'snapshot "$0"' '{}' \;
  cp -R "$directory/"* "$backup_directory"
else
  find "$directory" -type d -exec bash -c 'createfolders "$0"' '{}' \; #create function errr which changes to newpath
  find "$directory" -type f -exec bash -c 'checking "$0"' '{}' \;
  moving_files ; moving_folders
  find "$temporary_folder" -mtime "+$time_of_life" -exec rm -rf '{}' \; #remove files older than 7 days in LOST+FOUND
fi
exit 0
