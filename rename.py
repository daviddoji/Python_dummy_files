# -*- coding: utf-8 -*-
import glob

initial_ext = raw_input("Enter extension of raw files to be \
                        rename(.txt, .pdf, .dat, ...): ")
lof = "*" + initial_ext
#final_ext = raw_input("Enter desired extension (.txt, .edf, .dat, ...): ")
file_list = glob.glob(lof)
for files in file_list:
    files.split()
    files = files.replace(" ", "_")
    files = files.replace(",", "")
    files = files.replace("ñ", "n")
    print files

    