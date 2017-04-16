# TO USE THIS SCRIPT
# 




import sys, os
import numpy as np
import fabio
import pyFAI


#base_dir = '/data/id13/inhouse3/THEDATA_I3_1/d_2015-12-03_inh_ih_sc1303/PROCESS/'
#poni = base_dir + 'SESSION2/Al2O3_PE_0000.poni'
#mask = base_dir + 'SESSION00/MASK_PE_0000.edf'
#savename = '/data/id13/inhouse3/THEDATA_I3_1/d_2015-12-03_inh_ih_sc1303/PROCESS/SESSION00/PE_2000Kps_360ms_557.txt'
# -----------------------------------------------------------------------------#
#azmin, azmax = -180, 180
#smin, smax   = 0.025, 1 
#qmin, qmax   = 0.1, 55
#npt          = 4000
# -----------------------------------------------------------------------------#

def integrate1d(file_list):
    """ """
    base_dir = raw_input("Enter Base Directory:   ")
    poni     = base_dir + "/" + raw_input("Enter PONI-File (relative to Base Directory):   ")
    mask     = base_dir + "/" + raw_input("Enter MASK-File(relative to Base Directory):   ")
    savename = base_dir + "/" + raw_input("ENTER File name to save the data (relative to Base Directory):   ") +".edf"
    qmin     = 62.83185195922852 * float(raw_input("Enter the minimum s-value (A):   "))
    qmax     = 62.83185195922852 * float(raw_input("Enter the maximum s-value (A):   "))
    azmin    = float(raw_input("Enter minimum azimutal angle (deg):   "))
    azmax    = float(raw_input("Enter maximum azimutal angle (deg):   "))
    npt      = int(raw_input("Enter number of points along s axis:   "))
    
    
    
    ai = pyFAI.azimuthalIntegrator.AzimuthalIntegrator()
    ai.load(poni)
    ai.set_maskfile(mask)

    I_arr = np.zeros((len(file_list)+1, npt))
 

    
    for i in range(len(file_list)):
        data = fabio.open(file_list[i]).data

        q, I = ai.integrate1d(data,
                              npt=npt,
                           #   filename=filename
                              correctSolidAngle=False,
                              variance=None, error_model=None,
                              radial_range=(qmin, qmax),
                              azimuth_range=(azmin, azmax),
                           #   mask=None, 
                              dark=None, flat=None,
                              dummy=-5,
                              method="bbox",
                              unit="q_nm^-1",
                              safe=True,
                              normalization_factor=None)
                          
        I[I == -5] = np.nan
                
        I_arr[i+1,] = I
 
        T_arr = I_arr.T
    
 
    q = q/62.83185195922852
    I_arr[0,] = q
    
    
    img = fabio.open(file_list[0])
    img.data = I_arr
    print "Save integrated 2D Data to:", savename
    img.write(savename)
    
    
    
#    np.savetxt(savename, T_arr, delimiter='\t') 
	
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python integrate1d <files>"
        sys.exit(0)
    
    integrate1d(sys.argv[1:])        
    
    
    
