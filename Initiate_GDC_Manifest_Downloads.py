#!/home/ectroudt/anaconda3/bin/python3.6

import subprocess
import argparse


def main():

    parser = argparse.ArgumentParser(description="Retrieve Location and Run info")

    # Add command line argument for ABSOLUTE path to directory containing all Project files
    parser.add_argument("man_Folder", type=str, nargs="?",
                        help="Directory location of folder containing manifest and all other relevant project files")

    # Add command line argument for whether first or second half of Manifest Folder is being processed
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--first_run", dest="run_status", action="store_true",
                       help="Determine if working on first or second half on Manifest folder")
    group.add_argument("--second_run", dest="run_status", action="store_false",
                       help="Determine if working on first or second half on Manifest folder")

    # Is first time processing BAM files unless --second_run is passed
    parser.set_defaults(run_status=True)

    prog_Args = parser.parse_args()

    # Run GDC_Manifest_Process.py to begin downloading BAM files thru gdc-client
    program = "/home/ectroudt/anaconda3/bin/python3.6"
    program_code = "/home/ectroudt/TCGA_Code/GDC_Data_Processing/GDC_Manifest_Process.py"
    program_arg_1 = str(prog_Args.man_Folder)
    program_arg_2 = prog_Args.run_status
    screen_name = "Manifest_Download_Session"

    subprocess.Popen(["screen", "-S", screen_name, "-d", "-m", program, program_code, program_arg_1, program_arg_2])

    print("gdc-client and salmon processes are starting from screen session:  \n")
    subprocess.call(["screen", "-ls"])


if __name__ == '__main__':
    main()
