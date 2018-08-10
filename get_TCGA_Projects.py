#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import subprocess

projects_dir = str(sys.argv[1])

with open(projects_dir) as projects:

    ind_projects = projects.readlines()

for rec in ind_projects:

    rec = str(rec.rstrip("\n"))
    subprocess.call(["/home/ectroudt/TCGA_Code/GDC_Data_Processing/GDC_API_Data_Aquisition.py", rec])

