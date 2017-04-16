# -*- coding: utf-8 -*-
import glob
import PyPDF2 as pyPdf
# from pyPdf import PdfFileReader


# files sorted in a ascending way
file_list = sorted(glob.glob("*.pdf"))

# loop through all files in the list
for filename in file_list:
    # open the file
    with open(filename) as f:
        # read the pdf file
        f = pyPdf.PdfFileReader(open(filename, 'rb'))
        # get the number of pages
        dummy = f.getNumPages()

        print(filename + ' tiene ' + str(dummy) + ' páginas')
