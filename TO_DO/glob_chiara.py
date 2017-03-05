filimport glob 
file_list = glob.glob("*.edf")
# print(file_list)
for index, image in enumerate((file_list)):
	poni_file = "AgBh_Al2O3_detx0.poni"
        image_file = "image"
        target_2th = 11.5
              import numpy, fabio, pyFAI
              img = fabio.open(image)
              ai = pyFAI.load(poni_file)
              I, tth, chi = ai.integrate2d(img.data, 1000, 360, unit="2th_deg")
              selected_col = numpy.argmin(abs(tth-target_2th))
              prof = I[:, selected_col]
              numpy.savetxt("raw_RDG_1_166_1_167_%i.txt" %index, numpy.transpose((chi, prof)))
