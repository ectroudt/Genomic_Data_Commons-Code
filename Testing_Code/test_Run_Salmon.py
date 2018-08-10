#!/home/ectroudt/anaconda3/bin/python3.6

import sys

sys.path.insert(0, "/home/ectroudt/TCGA_Code/GDC_Data_Processing/")

from GDC_Manifest_Process import run_Salmon


def main():

    run_Salmon()


if __name__ == '__main__':

    main()