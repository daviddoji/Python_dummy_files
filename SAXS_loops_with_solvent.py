from __future__ import division
from shutil import copyfile
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import fileinput
import sys

### Pylab mode should be disabled ##############################################
### USE interactive(Qt4) AS PYLAB BACKEND ######################################

################################################################################
### Function definitions

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")



def fig(x,y, title, xscale='log', yscale='log', xlim=(0.009, 0.55),
        ylim=(0.2, 2200), xlabel='q [A$^{-1}$]', ylabel='I(q) [a.u.]'):
    """ Plot a figure consisting in one set of data"""
    plt.figure()
    plt.plot(x, y, label=temp_range)
    plt.title(title)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    # Remove the whitespace around the image.
    #plt.savefig(title + '.png', bbox_inches='tight')
    plt.show()


def fig2(x,y, title, xscale='log', yscale='log', xlim=(0.009, 0.55),
        ylim=(0.2, 2200), xlabel='q [A$^{-1}$]', ylabel='I(q) [a.u.]', 
        **kwargs):
    """ Plot a figure consisting in two sets of data"""
    plt.figure()
    plt.plot(x, y)
    for arg, value in kwargs.items():
        if arg == 'w':
            w = value
            continue
        z = value
    plt.plot(w, z, 'bo', linewidth=2.5)
    plt.title(title)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # Remove the whitespace around the image.
    #plt.savefig(title + '.png', bbox_inches='tight')
    plt.show()

#fig2(samples_q, intens_reshaped,
#    'Samples norm. after subtraction of the solvent',
#    w=ref_q[:,0], z=ref)


def find_nearest(array, value):
    """ Return the closest index position of a value in an array"""
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


# Are the edf files here?
dummy = raw_input("Make sure there is a folder with edf files along with "
                  "the integrated .dat files (press Enter to proceed)")
del dummy


# REMOVE HEADERS ###############################################################
# extension of the files where the data are
ending = raw_input("Extension of raw files (.txt, .edf, .dat, ...): ")
lof = "*" + ending
# extension desired for files
#final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
# files sorted in a ascending way
files_list = sorted(glob.glob(lof))


# loop through all files in the list
for file_name in files_list:
    # split name of file in root + ext
    root, ext = os.path.splitext(file_name)
    # make a copy of the files
    file_cleaned = root + "_cln" + ending
    copyfile(file_name, file_cleaned)
    # read every line of the file and do not display any output
    for line in fileinput.input([file_cleaned], inplace=True):
        # if first character is a number
        if line[0].isdigit():
            # print line without appending newline at the end ","
            print line,

# delete useless variables
del ending, lof, files_list, file_name, root, ext, file_cleaned, line 


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
ref_q = ref_q_wo_NaNs.reshape((num_rows_R, num_cols_R), order='F')

# average intensity values
ref_I = np.average(ref_intens_reshaped, axis=1)

# delete useless variables
del ref_data, filename, ref_files, f, line, columns, rows, x
del num_cols_R, ref_intens, ref_q_wo_NaNs, ref_intens_wo_NaNs
del ref_intens_reshaped # ???



## SOLVENT CORRECTIONS FOR DIFFERENT TEMPERATURES ##############################
temp_range = raw_input("What are the temperatures measured (enter values "
                       "separated by commas): ")

temp_range = np.array(temp_range.split(","), dtype=np.int8)


solvent_T = np.column_stack([ref_I 
                            * (1 - (0.00359 * (temp_range[0] - temp_range[i]))) 
                            for i in range(len(temp_range))])

# delete useless variables
del i

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
samples_I= intens_wo_NaNs.reshape((num_rows_S, num_cols_S), order='F')
samples_q = q_wo_NaNs.reshape((num_rows_S, num_cols_S), order='F')

# delete useless variables
del samples_data, filename, sample_files, f, line, columns, rows, x
del q, intens, q_wo_NaNs, intens_wo_NaNs


# plot intensity vs q with solvent on the graph
fig2(samples_q, samples_I,'Samples and Solvent', ylim=(0.2, 2500),
    w=ref_q[:,0], z=ref_I)


# ask for the minimum
dummy = raw_input("Check the minimum Intensity value for the following graphs "
                  "(press Enter to display)")
del dummy


# plot intensity vs q
fig2(samples_q, samples_I,'Samples', ylim=(0.2, 2500),
    w=samples_q[:,0], z=samples_I[:, num_cols_S-1])


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

# MAKE SURE THAT THE ARRAYS ARE EQUALS IN LENGTH ###############################

if len(samples_q) != len(ref_q):
    samples_q = samples_q[1:, :]
    samples_I= samples_I[1:, :]

################################################################################

minimum = float(raw_input("What was the Intensity of your minimum? "))

# get the index of the minimum value previously specified
min_index = find_nearest(samples_I[:, num_cols_S-1], minimum)


# for slicing
start_min = min_index-15
stop_min = min_index+15



ref_corr = []

for i in range(num_cols_S):
    dummy = samples_I[start_min:stop_min, i]
    dummy_solvent = solvent_T[start_min:stop_min, i]
    scaling_factor = np.average(dummy / dummy_solvent, axis=0)
    solvent_scaled = solvent_T[:, i] * scaling_factor
    ref_corr.append(solvent_scaled)
    #print len(i)

# cast data list into an array
ref_corr = np.array(ref_corr)
ref_corr = ref_corr.T

# delete useless variables
del minimum, min_index, start_min, stop_min
del i, dummy, dummy_solvent, scaling_factor, solvent_scaled, 

### compared solvent before and after correction    
fig2(samples_q[:,0], solvent_T[:,0],'Solvent before and after rescaling',
    ylim=(0.2, 25), w=samples_q[:,0], z=ref_corr[:,0])

################################################################################

# subtract solvent from samples
samples_sub = samples_I - ref_corr

fig(samples_q, samples_sub,'Samples after solvent subtraction',
    ylim=(0.01, 3000))


# ask for the minimum
dummy = raw_input("Check the Intensity value of the minimum before the peak "
                  "for the following graphs (press Enter to display)")
del dummy

# NORMALIZED SAMPLES INTENSITY BY HIGH TEMP MEASUREMENT ########################

samples_sub_norm = samples_sub / samples_sub[:, 0, np.newaxis]


fig2(samples_q, samples_sub_norm,'Samples normalized', ylim=(0.01, 30),
    w=samples_q[:,0], z=samples_sub_norm[:,3])
    

################################################################################

minimum2 = float(raw_input("What was the Intensity of your minimum? "))

# get the index of the minimum value previously specified
min2_index = find_nearest(samples_sub_norm[:, num_cols_S//2], minimum2)

# for slicing
start_min = min2_index-15
stop_min = min2_index+15

# slice only around the minimum value
avg_samples_sub_norm = samples_sub_norm[start_min:stop_min]

# average the columns???
avg_samples_sub_norm = np.average(avg_samples_sub_norm, axis=0)


#intens_ref_subtracted_norm = samples_sub_norm / avg_samples_sub_norm
samples_sub_norm_avg = samples_sub_norm / avg_samples_sub_norm


# delete useless variables
del minimum2, min2_index, start_min, stop_min, avg_samples_sub_norm


# ask for the maximum
dummy = raw_input("Check the Intensity value of the peak "
                  "for the following graphs (press Enter to display)")
del dummy

fig2(samples_q, samples_sub_norm_avg,
    'Samples norm. after subtraction of the solvent', ylim=(0.7, 30),
    w=samples_q[:,0], z=samples_sub_norm_avg[:,3])


maximum = float(raw_input("What was the Intensity of your maximum? "))

# get the index of the maximum value previously specified
max_index = find_nearest(samples_sub_norm_avg[:, num_cols_S//2], maximum)


# for slicing
start_max = max_index-15
stop_max = max_index+15


# slice only around the maximum value
first_peak = samples_sub_norm_avg[start_max:stop_max]

# average the columns???
first_peak_position = np.average(first_peak, axis=0)

# delete useless variables
del maximum, max_index, start_max, stop_max, num_cols_S
del first_peak

# save the arrays
q = samples_q[:, 0, np.newaxis]
I = samples_sub_norm_avg
save_arrays = np.hstack((q, I))
dummy = raw_input("Name for the output .txt file? ")
np.savetxt(dummy, save_arrays, delimiter='\t', newline='\r\n',
            fmt='%.5f', header='q [A-1], I [a.u.]')

del q, I, save_arrays, dummy


# delete all files without headers
filelist = glob.glob('*cln.dat')
for f in filelist:
    os.remove(f)

# delete useless variables
del filelist, f