from __future__ import division
from shutil import copyfile
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import fileinput


### Pylab mode should be disabled ##############################################
### USE interactive(Qt4) AS PYLAB BACKEND ######################################

# Are the edf files here?
dummy = raw_input("Make sure there is a folder with edf files along with "
                  "the integrated .dat files (press Enter to proceed)")
del dummy


# REMOVE HEADERS ###############################################################
# extension of files to change
initial_ext = raw_input("Extension of raw files (.txt, .edf, .dat, ...): ")
lof = "*" + initial_ext
# extension desired for files
final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
# files sorted in a ascending way
files_list = sorted(glob.glob(lof))


# loop through all files in the list
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

# delete useless variables
del initial_ext, lof, final_ext, root, ext, file_cleaned, line, files_list


# SEPARATE SAMPLES FROM REFERENCES #############################################
# separate reference files from sample files
ref = "*" + raw_input("Enter first reference number: ") + "_cln*"
ref = glob.glob(ref)[0]
num_refs = int(raw_input("How many references are there? "))

all_files = sorted(glob.glob('*_cln.dat'))
first_ref = all_files.index(ref)
ref_files = all_files[first_ref:first_ref+num_refs]

sample_files = all_files

# delete useless variables
del sample_files[first_ref:first_ref+num_refs]
del ref, num_refs, all_files, first_ref

# GET REFERENCES DATA AND MAKE AVERAGE #########################################
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

# delete useless variables
del ref_data, filename, ref_files, f, line, columns, rows,x
del ref_q, ref_intens, ref_q_wo_NaNs, ref_intens_wo_NaNs


## SOLVENT CORRECTIONS FOR DIFFERENT TEMPERATURES ###############################
##initial_temp = float(raw_input("What is the initial temperature? "))
#
#temp_range = raw_input("What are the temperatures measured (enter values "
#                       "separated by commas): ")
#
#temp_range = np.array(temp_range.split(","), dtype=np.int8)
#
#
#solvent_T = np.column_stack([ref_intens_reshaped 
#                            * (1 - (0.00359 * (temp_range[0] - temp_range[i]))) 
#                            for i in range(len(temp_range))])
#

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

# delete useless variables
del samples_data, filename, sample_files, f, line, columns, rows, x
del q, intens, q_wo_NaNs, intens_wo_NaNs


# ask for the minimum
dummy = raw_input("Check the minimum Intensity value for the following graphs "
                  "(press Enter to display)")
del dummy


# plot intensity vs q
plt.figure()
plt.plot(q_reshaped, intens_reshaped)
plt.plot(q_reshaped[:,0], intens_reshaped[:, num_cols_S-1],'bo')
plt.title('Samples')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
#plt.savefig('Samples.png', bbox_inches='tight') 
plt.show()

################################################################################
## files sorted in a ascending way
#edf_list = sorted(glob.glob('**/*.edf'))
#
#counts = []
#
##for file_name in test:
#for file_name in edf_list:
#    # open the file
#    with open(file_name) as f:
#        text = f.readlines()
#        dummy = text[22].split()
#        #dummy = f.readlines()[22].split()
#        value = int(dummy[2])
#        # append rows to data
#        counts.append(value)
#        
#
#counts_ref = 18292660
#
#cor_coef = []
#for i in range(len(counts)):
#    cor_coef.append(float(counts_ref)/counts[i])
#
#
#intens_reshaped_cor = intens_reshaped * cor_coef
#
## delete useless variables
#del edf_list, file_name, f, text, dummy, value, counts_ref, i
################################################################################

# NORMALIZED SAMPLES INTENSITY BY SOLVENT AND DISPLAY THEM #####################

if len(q_reshaped) != len(ref_q_reshaped):
    q_reshaped = q_reshaped[1:, :]
    intens_reshaped = intens_reshaped[1:, :]

# normalize samples intensity by the solvent intensity
intens_reshaped_ref_norm = intens_reshaped / ref[:,np.newaxis]

## make the average of each sample intensities
##avg_intensity_reshaped_solvent_nor = np.average(intensity_reshaped_solvent_norm,
##                                                axis=1)
#
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
start_min = min_index-15
stop_min = min_index+15

# slice only around the minimum value
avg_intens_reshaped_ref_nor = intens_reshaped_ref_norm[start_min:stop_min]

# average the slice by columns
avg_intens_reshaped_ref_nor = np.average(avg_intens_reshaped_ref_nor, axis=0)

# normalize by the previous average
intens_reshaped_ref_norm_avg = intens_reshaped_ref_norm / avg_intens_reshaped_ref_nor

# delete useless variables
del minimum, min_index, start_min, stop_min, avg_intens_reshaped_ref_nor
del intens_reshaped_ref_norm

# plot intensity vs q normalized by the solvent
plt.figure()
plt.plot(q_reshaped, intens_reshaped_ref_norm_avg)
#plt.plot(ref_q_reshaped[:,0], ref, 'r--')
plt.title('Samples normalized by solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.3, 1700)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
#plt.savefig('Samples normalized by solvent.png', bbox_inches='tight')
plt.show()


# ask for the minimum
dummy = raw_input("Check the Intensity value of the minimum before the peak "
                  "for the following graphs (press Enter to display)")
del dummy


# SUBTRACT THE SOLVENT AND DISPLAY THEM ########################################

intens_ref_subtracted = intens_reshaped_ref_norm_avg \
                        / intens_reshaped_ref_norm_avg[:,0,np.newaxis]

# plot intensity vs q after subtraction the solvent
plt.figure()
plt.plot(q_reshaped, intens_ref_subtracted)
plt.title('Samples after subtraction of solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.02, 1.5)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
#plt.savefig('Samples after subtraction of solvent.png', bbox_inches='tight')
plt.show()

################################################################################

minimum2 = float(raw_input("What was the Intensity of your minimum? "))

# get the index of the minimum value previously specified
min2_index = find_nearest(intens_ref_subtracted[:, num_cols_S//2], minimum2)


# for slicing
start_min = min2_index-15
stop_min = min2_index+15

# slice only around the minimum value
avg_intens_ref_subtracted = intens_ref_subtracted[start_min:stop_min]

# average the columns???
avg_intens_ref_subtracted = np.average(avg_intens_ref_subtracted, axis=0)


intens_ref_subtracted_norm = intens_ref_subtracted / avg_intens_ref_subtracted


# delete useless variables
del minimum2, min2_index, start_min, stop_min, avg_intens_ref_subtracted

plt.figure()
plt.plot(q_reshaped, intens_ref_subtracted_norm)
plt.title('Samples norm. after subtraction of the solvent')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.ylim(0.7, 30)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
# Remove the whitespace around the image.
#plt.savefig('Samples norm. after subtraction of solvent.png', bbox_inches='tight')
plt.show()


# save the arrays
q = q_reshaped[:, 0, np.newaxis]
I = intens_ref_subtracted_norm
save_arrays = np.hstack((q,I))
dummy = raw_input("Name for the output .txt file? ")
np.savetxt(dummy, save_arrays, delimiter='\t', newline='\r\n',
            fmt='%.5f', header='q [A-1],I [a.u.]')

del q, I, save_arrays, dummy


# delete all files without headers
filelist = glob.glob('*cln.dat')
for f in filelist:
    os.remove(f)

# delete useless variables
del filelist, f
