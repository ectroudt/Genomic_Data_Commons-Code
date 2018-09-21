#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import os
import argparse
import bam_fq, tools

parser = argparse.ArgumentParser(description="Retrieve current split and split number")

parser.add_argument("current_Split", type=int, nargs="?", choices=range(1, 7), help="Current split number")

parser.add_argument("--split_Num", type=int, nargs="?", choices=range(2, 7), default=6,
                        help="Argument to determine number of salmon processes that will run in parallel")

Args = parser.parse_args()

if Args.current_Split > Args.split_Num:
    print("Current split number is greater than number of splits...Incompatible")
    sys.exit()

j = Args.current_Split
s = (Args.split_Num - 1)

indirname = ""
preprefix = ""
indexname = '/home/ectroudt/salmon_Data/index_ensembl_salmon_quasi_NewVers'


for project_folder in os.listdir("/data/rnaSeq/TCGA_Projects/"):

    if "TCGA" in str(project_folder):

        project_Dir = os.path.join("/data/rnaSeq/TCGA_Projects/", project_folder)

        for data_Dir in os.listdir(project_Dir):

            if "download" in str(data_Dir):

                indirname = os.path.join(project_Dir, data_Dir) + "/"

            else:

                preprefix = os.path.join(project_Dir, data_Dir) + "/"


indirs = [indirname+x for x in os.listdir(indirname) if 'manifest' not in x]
indirs = sorted(indirs)
x = len(indirs)

ndirs = indirs[(j-1)*int(x/s):j*int(x/s)]
bf = bam_fq.Bam_fq()
tl = tools.Tools()

for ndir in ndirs:
    print(ndir)
    ndir += '/'
    ubamfile = [ndir + x for x in os.listdir(ndir) if '.bam' in x and 'sorted' not in x][0]
    prefix = preprefix + ubamfile.split('/')[-1].replace('.bam', '')

    print(ubamfile)
    print('sorting bam:')
    sbamfile = bf.bam_to_sorted_bam(ubamfile)
    sbamfile = ubamfile.replace('.bam', '.sorted.bam')
    bf.remove_file(ubamfile)
    print(sbamfile)
    
    print('bam to one fq:')
    fq = ubamfile.replace('.bam', '.fq')
    fq = bf.sorted_bam_to_fq(sbamfile)
    bf.remove_file(sbamfile)
    print(fq)
    
    print('split and sort fq')
    fq1, fq2 = bf.split_and_sort_fq(fq)
    bf.remove_file(fq)
    print(fq1)
    print(fq2)
    
    print('process salmon')
    tl.salmon(fq1, fq2, indexname, prefix)
    bf.remove_file(fq1)
    bf.remove_file(fq2)

    bf.remove_file(ndir)
    print('next')