#!/home/ectroudt/anaconda3/bin/python3.6

import subprocess


screen_name = "test_Code"
program = "/home/ectroudt/anaconda3/bin/python3.6"
program_code = "/home/ectroudt/TCGA_Code/GDC_Data_Processing/Testing_Code/check_for_incomplete_downloads.py"
program_arg = "/home/ectroudt/TCGA_Projects_Processed/"

test_Obj = subprocess.run([program, program_code, program_arg],
               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

if not test_Obj.stderr:

    print(test_Obj.stdout)

else:

    print("Error found : " + str(test_Obj.stderr))

