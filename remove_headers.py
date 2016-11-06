import glob, os, fileinput
from shutil import copyfile

# extension of files to change
initial_ext = raw_input("Enter extension of raw files (.txt, .edf, .dat, ...): ")
lof = "*" + initial_ext
# extension desired for files
final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
# files sorted in a ascending way 
file_list = sorted(glob.glob(lof))


for file_name in file_list:
    # split name of file in root + ext
    root, ext = os.path.splitext(file_name)
    # make a copy of the files
    file_cleaned = root + "_cln" + final_ext
    copyfile(file_name, file_cleaned)
    # read every line of the file and do not display any output
    for line in fileinput.input([file_cleaned], inplace=True):
        # if first character is a number
        if line[0].isdigit():
            # print line without appending newline at the end ","
            print line,