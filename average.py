# -*- coding: utf-8 -*-
import glob
import numpy as np

# create a list with all files in the directory
file_list = glob.glob("*.dat2")

# store intensity values
intensity = []

# loop through all files in the list
for filename in file_list:

    # skip 30 rows for the headers and use only columns 0 (q_values) and 1 (intensity_values)
    myarray = np.loadtxt(filename, skiprows=30, usecols=(0,1))

    # remove all the rows where the second column (intensity_values) is nan
    myarray = myarray[~np.isnan(myarray[:,1])]

    # append intensity values to avg list
    intensity.append(myarray[:,1])

# average intensity values
solvent = sum(intensity)/len(file_list)
print solvent
