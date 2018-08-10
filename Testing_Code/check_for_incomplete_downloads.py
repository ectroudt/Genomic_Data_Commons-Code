#!/home/ectroudt/anaconda3/bin/python3.6


import os
import sys


pcount = 0

# Check the current /data/rnaSeq/TCGA_Projects/TCGA-** directory for '.partial' files
for man_files in os.listdir(sys.argv[1]):

    man_dir = os.path.join(sys.argv[1], man_files)

    for data_files in os.listdir(man_dir):

        if ".partial" in str(data_files):

            print(str(data_files))
            pcount += 1

        else:

            pass


print("Number of incomplete BAM files: " + str(pcount))

