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


# ask for the minimum
dummy = raw_input("Check the minimum Intensity value for the following graphs "
                  "(press Enter to display)")
del dummy


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
# plt.savefig('Samples.png', bbox_inches='tight')
plt.show()



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
ref_intens_reshaped = ref_intens_wo_NaNs.reshape((num_rows_R, num_cols_R), order='F')
ref_q_reshaped = ref_q_wo_NaNs.reshape((num_rows_R, num_cols_R), order='F')

# average intensity values
ref = np.average(ref_intens_reshaped, axis=1)


# plot intensity vs q with solvent on the graph
plt.figure()
plt.plot(q_reshaped, intens_reshaped)
plt.plot(ref_q_reshaped[:,0], ref, 'r--')
plt.title('Samples and Solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
plt.show()



# NORMALIZED SAMPLES INTENSITY BY SOLVENT AND DISPLAY THEM #####################

if len(q_reshaped) != len(ref_q_reshaped):
    q_reshaped = q_reshaped[1:, :]
    intens_reshaped = intens_reshaped[1:, :]

# normalize samples intensity by the solvent intensity
intens_reshaped_ref_norm = intens_reshaped / ref[:,np.newaxis]

# make the average of each sample intensities
#avg_intensity_reshaped_solvent_nor = np.average(intensity_reshaped_solvent_norm,
#                                                axis=1)

################################################################################
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    #return array[idx]
    return idx

#array = np.random.random(10)
#print(array)
## [ 0.21069679  0.61290182  0.63425412  0.84635244  0.91599191  0.00213826
##   0.17104965  0.56874386  0.57319379  0.28719469]
#
#value = 0.5
#
#print(find_nearest(array, value))
################################################################################

minimum = float(raw_input("What was the Intensity of your minimum? "))

# get the index of the minimum value previously specified
min_index = find_nearest(intens_reshaped[:, num_cols_S-1], minimum)


# for slicing
start_min = min_index-100
stop_min = min_index+100

# slice only around the minimum value
avg_intens_reshaped_ref_nor = intens_reshaped_ref_norm[start_min:stop_min]

# average the columns???
avg_intens_reshaped_ref_nor = np.average(avg_intens_reshaped_ref_nor, axis=0)

#
intens_reshaped_ref_norm_avg = intens_reshaped / avg_intens_reshaped_ref_nor


# plot intensity vs q normalized by the solvent
plt.figure()
plt.plot(q_reshaped, intens_reshaped_ref_norm_avg)
plt.plot(ref_q_reshaped[:,0], ref, 'r--')
plt.title('Samples normalized by solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.3, 230)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
#plt.savefig('Samples normalized by ref.png', bbox_inches='tight')
plt.show()



# SUBTRACT THE SOLVENT AND DISPLAY THEM ########################################

intens_ref_subtracted = intens_reshaped_ref_norm_avg - ref[:,np.newaxis]
plt.figure()
plt.plot(q_reshaped, intens_ref_subtracted)
plt.title('Samples after subtraction of the solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.02, 230)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
plt.show()


# ask for the minimum
dummy = raw_input("Check the q value of the minimum before the peak for the "
                  "following graphs (press Enter to display)")
del dummy




# NORMALIZE BY FIRST COLUMN OF SHEET 4 #########################################

structure_factor = intens_ref_subtracted / intens_ref_subtracted[:, 0, np.newaxis]
plt.figure()
plt.plot(q_reshaped, structure_factor)
plt.plot(q_reshaped[:, 0], structure_factor[:, num_cols_S-1], 'bo', 
        linewidth=2.5)
plt.title('Structure factor')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.02, 230)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
plt.show()



# NORMALIZE BY THE MEAN OF SHEET 5 #############################################

minimum2 = float(raw_input("What was the q value for the minimum? "))

# get the index of the minimum value previously specified
min2_index = find_nearest(q_reshaped[:, num_cols_S-1], minimum2)


# for slicing
start_min2 = min2_index-5
stop_min2 = min2_index+5

# slice only around the minimum value
structure_factor_slice = structure_factor[start_min2:stop_min2]

# average the columns???
structure_factor_avg = np.average(structure_factor_slice, axis=0)

# standard deviation
structure_factor_std = np.std(structure_factor_slice, axis=0)


structure_factor_rescaled = structure_factor / structure_factor_avg


# ask for the minimum
dummy = raw_input("Check the Intensity value of the peak for the "
                  "following graphs (press Enter to display)")
del dummy


# plot the Structure Factore rescaled
plt.figure()
plt.plot(q_reshaped, structure_factor_rescaled)
plt.plot(q_reshaped[:, 0], structure_factor_rescaled[:, num_cols_S-1], 'bo', 
        linewidth=2.5)
plt.title('Rescaled Structure factor')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.02, 230)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
plt.show()



# GET THE MAXIMUM FOR THE STRUCTURE FACTOR #####################################
maximum = float(raw_input(" What was the Intensity of your peak? "))

# get the index of the minimum value previously specified
max_index = find_nearest(structure_factor_rescaled[:, num_cols_S-1], maximum)


# for slicing
start_max = max_index-5
stop_max = max_index+5


# slice only around the minimum value
dummy_slice = structure_factor_rescaled[start_max:stop_max]
# average the columns???
dummy_avg = np.average(dummy_slice, axis=0)
# standard deviation
dummy_std = np.std(dummy_slice, axis=0)

# array for time
test = np.arange(len(dummy_avg))

# plot the first peak for the Structure Factore
plt.figure()
#plt.plot(test, dummy_avg, 'bs')
plt.errorbar(test, dummy_avg, yerr=dummy_std, fmt='o', ecolor='red')
plt.title('Kinetics')
plt.xlim(-0.5, len(dummy_avg)+1)
plt.xlabel('Time [min]')
plt.ylabel('Structure factor (1$^{st}$ peak)')
plt.show()


### SAVE THE ARRAYS INTO A TXT FILE ############################################
#x = y = np.arange(0.0,11.0,0.5)

z = np.array(zip(test, dummy_avg))

savename = raw_input("Name and extension for the file to save: ")

np.savetxt(savename, z, delimiter='\t', newline='\r\n', 
           fmt='%.6f', header='q [A-1]\tStr. Factor')
