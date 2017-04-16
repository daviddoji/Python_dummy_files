import os
import glob
import shutil

# files sorted in a ascending way
files_list = sorted(glob.glob('*.dat'))

# files per folders
files_in_folders = int(raw_input("How many files should be in each folder? "))

# number of folders to create
folders = len(files_list)/files_in_folders

# working directory
pwd = os.getcwd()

# Folders' name to be created
current_path = pwd+'/Loop'


for i in range(folders):
    # append number to Folders' name
    newpath = current_path + str(i+1)
    # make sure it doesn't exist 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # group files in the created folders
    for p in range(files_in_folders):
        shutil.move(files_list[0], newpath)
        del files_list[0]

# delete variables
del i, p
del pwd, current_path, newpath
del folders, files_in_folders

# delete files in working directory
#for f in files_list:
#    os.remove(f)

del files_list
