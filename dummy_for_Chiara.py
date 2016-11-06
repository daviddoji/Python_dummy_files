import glob, os, fileinput
initial_ext = raw_input("Enter extension of raw files (.txt, .edf, .dat, ...): ")
lof = "*" + initial_ext
final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
file_list = glob.glob(lof)

headers = "#\n" * 17

for index, file_name in enumerate((file_list)):
    for line in fileinput.input([file_name], inplace=True):
        if fileinput.isfirstline():
            print headers,
        print line,
    pre, ext = os.path.splitext(file_name)
    os.rename(file_name, pre + final_ext)      
