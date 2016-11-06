from __future__ import division
import glob
import numpy as np
import matplotlib.pyplot as plt

# separate solvent files from sample files
ref = "*" + raw_input("Enter first reference number: ") + "*"
ref = glob.glob(ref)[0]
num_refs = int(raw_input("How many references are? "))

all_files = sorted(glob.glob('*_cln.dat'))
first_ref = all_files.index(ref)
ref_files = all_files[first_ref:first_ref+num_refs]

sample_files = all_files
del sample_files[first_ref:first_ref+num_refs]
del all_files


# files sorted in a ascending way 
#file_list_cleaned = sorted(glob.glob("*_cln.dat"))

# original raw_data with NaNs
data = []

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
            data.append(rows)
            
# cast data list into an array
data = np.array(data)
# slice q values from the list
q = data[:,0]
# slice intensity values from the list
intensity = data[:,1]

# remove all the rows where the second row value (intensity) is nan
q_wo_NaNs = q[~np.isnan(intensity)]
intensity_wo_NaNs = intensity[~np.isnan(intensity)]

# for reshaping
#num_rows = len(file_list_cleaned)
num_rows = len(sample_files)
num_cols = len(intensity_wo_NaNs)/len(sample_files)

# store data in different arrays
intensity_reshaped = intensity_wo_NaNs.reshape((num_rows, num_cols))
q_reshaped = q_wo_NaNs.reshape((num_rows, num_cols))

# plot intensity vs q
plt.figure()
plt.plot(q_reshaped.T, intensity_reshaped.T)
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.009, 0.55)
plt.xlabel('q [A$^{-1}$]')
plt.ylabel('Intensity [a.u.]')
plt.show()