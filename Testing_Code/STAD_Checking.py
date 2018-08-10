#!/home/ectroudt/anaconda3/bin/python3.6


import os
import sys


salmon_Eq = []

# Check the current /data/rnaSeq/TCGA_Projects/TCGA-** directory for '.partial' files
for man_files in os.listdir(sys.argv[1]):

    man_dir = os.path.join(sys.argv[1], man_files)

    for data_files in os.listdir(man_dir):

        if "rehead.bam" in str(data_files):

            salmon_Eq.append(str(data_files)[:-4])


for abund_files in os.listdir(sys.argv[2]):

    if str(abund_files) in salmon_Eq:

        print("FOUND: " + str(abund_files) + " ******")



