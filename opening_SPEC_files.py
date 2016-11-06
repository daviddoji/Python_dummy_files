# -*- coding: utf-8 -*-
# Opening files

import csv
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


#file_name = raw_input("Enter filename for processing: ")
file_name = 'Au4.3nmPPh3_C16.spec'
filename, ext = os.path.splitext(file_name)

with open(file_name) as f:
    # skip 5 first lines for headers
    reader = f.readlines()[5:] 
    wavelength = []
    absorption = []
    
    try:
        for row in reader:
            row = row.strip()
            columns = row.split()
            wavelength.append(float(columns[0]))
            absorption.append(float(columns[1]))
            
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

# cast data into arrays and remove 100 first points
wavelength = np.array(wavelength[100:])
absorption = np.array(absorption[100:])

# plot absorption vs wavelength
plt.figure()
plt.plot(wavelength, absorption, "r-", label=filename)
plt.ylim(0, 0.85)
plt.xlim(310, 1110)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Absorbance')
plt.legend(loc='best')
plt.show()


# ask for the number of points
points = raw_input("How many points do you need? ")


#xnew = np.linspace(wavelength[0], wavelength[-1], points)
#test = interp1d(wavelength, absorption, kind='cubic')
#
#smooth = spline(wavelength, absorption, xnew)
#plt.plot(xnew, smooth, label='Smoothed')
#plt.plot(wavelength, test, "r-", label='Smoothed')

t_dummy = np.linspace(wavelength[0], wavelength[-1], len(wavelength))
t2_dummy = np.linspace(wavelength[0], wavelength[-1], points)

x2_dummy = np.interp(t2_dummy, t_dummy, wavelength)
y2_dummy = np.interp(t2_dummy, t_dummy, absorption)
sigma = 2
x3_dummy = gaussian_filter1d(x2_dummy, sigma)
y3_dummy = gaussian_filter1d(y2_dummy, sigma)

#x4_dummy = np.interp(t_dummy, t2_dummy, x3_dummy)
#y4_dummy = np.interp(t_dummy, t2_dummy, y3_dummy)


plt.figure()
plt.plot(wavelength, absorption, "o-", lw=2, label='raw_data')
plt.plot(x3_dummy, y3_dummy, "r", lw=2, label='Smoothed')
#plt.plot(x4_dummy, y4_dummy, "o")
plt.ylim(0, 0.85)
plt.xlim(310, 1110)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Absorbance')
plt.legend(loc='best')
plt.show()