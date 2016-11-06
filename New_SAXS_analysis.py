from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import glob, os, fileinput
from shutil import copyfile

### Pylab mode should be disabled ##############################################
### USE interactive(Qt4) AS PYLAB BACKEND ######################################

# REMOVE HEADERS ###############################################################
# extension of files to change
initial_ext = raw_input("Extension of raw files (.txt, .edf, .dat, ...): ")
lof = "*" + initial_ext
# extension desired for files
final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
# files sorted in a ascending way
files_list = sorted(glob.glob(lof))


for file_name in files_list:
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



# SEPARATE SAMPLES FROM REFERENCES #############################################
# separate reference files from sample files
ref = "*" + raw_input("Enter first reference number: ") + "_cln*"
ref = glob.glob(ref)[0]
num_refs = int(raw_input("How many references are there? "))

all_files = sorted(glob.glob('*_cln.dat'))
first_ref = all_files.index(ref)
ref_files = all_files[first_ref:first_ref+num_refs]

sample_files = all_files
del sample_files[first_ref:first_ref+num_refs]
del all_files



# GET REFERENCES DATA, MAKE AVERAGE AND DISPLAY THEM ###########################
# original raw_data with NaNs
ref_data = []

# loop through all sample files in the list
for filename in ref_files:
#for filename in file_list_cleaned:
    # open the file
    with open(filename) as f:
        # loop through all lines in the file
        for line in f:
            # split the line into columns
            columns = line.split()
            # cast columns values into float
            rows = [float(x) for x in columns]
            # append rows to data
            ref_data.append(rows)

# cast data list into an array
ref_data = np.array(ref_data)
# slice q values from the list
ref_q = ref_data[:,0]
# slice intensity values from the list
ref_intens = ref_data[:,1]

# remove all the rows where the second row value (intensity) is nan
ref_q_wo_NaNs = ref_q[~np.isnan(ref_intens)]
ref_intens_wo_NaNs = ref_intens[~np.isnan(ref_intens)]

# for reshaping
num_rows_R = int(len(ref_intens_wo_NaNs)/len(ref_files))
num_cols_R = int(len(ref_files))

# store data in different arrays
ref_intens_reshaped = ref_intens_wo_NaNs.reshape((num_rows_R, num_cols_R),
                      order='F')
ref_q_reshaped = ref_q_wo_NaNs.reshape((num_rows_R, num_cols_R), order='F')

# average intensity values
ref = np.average(ref_intens_reshaped, axis=1)



# SOLVENT CORRECTIONS FOR DIFFERENT TEMPERATURES ###############################
#initial_temp = float(raw_input("What is the initial temperature? "))

temp_range = raw_input("What are the temperatures measured (enter values "
                       "separated by commas): ")

temp_range = np.array(temp_range.split(","), dtype=np.int8)


solvent_T = np.column_stack([ref_intens_reshaped 
                            * (1 - (0.00359 * (temp_range[0] - temp_range[i]))) 
                            for i in range(len(temp_range))])


# GET SAMPLES DATA AND DISPLAY THEM ############################################
# original raw_data with NaNs
samples_data = []

# loop through all sample files in the list
for filename in sample_files:
#for filename in file_list_cleaned:
    # open the file
    with open(filename) as f:
        # loop through all lines in the file
        for line in f:
            # split the line into columns
            columns = line.split()
            # cast columns values into float
            rows = [float(x) for x in columns]
            # append rows to data
            samples_data.append(rows)

# cast data list into an array
samples_data = np.array(samples_data)
# slice q values from the array
q = samples_data[:,0]
# slice intensity values from the array
intens = samples_data[:,1]

# remove all the rows where the second row value (intensity) is nan
q_wo_NaNs = q[~np.isnan(intens)]
intens_wo_NaNs = intens[~np.isnan(intens)]

# for reshaping
num_rows_S = int(len(intens_wo_NaNs)/len(sample_files))
num_cols_S = int(len(sample_files))

# store data in different arrays
intens_reshaped = intens_wo_NaNs.reshape((num_rows_S, num_cols_S), order='F')
q_reshaped = q_wo_NaNs.reshape((num_rows_S, num_cols_S), order='F')

# plot intensity vs q
plt.figure()
plt.plot(q_reshaped, intens_reshaped)
plt.title('Samples')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
plt.savefig('Samples.png', bbox_inches='tight') 
plt.show()