#!/usr/bin/env bash

screen -S Process_BAM -d -m /home/ectroudt/anaconda3/bin/python3.6 /home/ectroudt/TCGA_Code/GDC_Data_Processing/GDC_Manifest_Process.py
/home/ectroudt/tcga_Project_Files

screen -S process_Salmon_UVM_1

python3.6 ~/TCGA_Code/GDC_Data_Processing/process_salmon_SEAN.py 3

rm -r ~/TCGA_Project_Test_Data/350fc705-cd79-427b-afb7-e6ebb929b43b/