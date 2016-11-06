#from __future__ import division
#import numpy as np
#import matplotlib.pyplot as plt
import glob, os, fileinput



# files sorted in a ascending way
files_list = sorted(glob.glob('*.edf'))

counts = []

for file_name in files_list:
    # open the file
    with open(file_name) as f:
        text = f.readlines()
        dummy = text[22].split()
        #dummy = f.readlines()[22].split()
        value = int(dummy[2])
        # append rows to data
        counts.append(value)


#f = open('dummy.edf')
#text = f.readlines()
#dummy = text[22].split()
#value = int(dummy[2])
#
#print value