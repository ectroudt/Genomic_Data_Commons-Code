#!/home/ectroudt/anaconda3/bin/python3.6

import subprocess
import argparse

# Call 'process_salmon_SEAN.py' to carry out salmon on downloaded BAM files
def initiate_Salmon(split_num):

    # split_num is set to 6 by default, unless different argument is passed
    split_num = int(split_num)
    split_num_call = str(split_num)

    for j in range(1, (split_num + 1)):

        scr_name = "salmon_processing_" + str(j)
        program_cmd = "/home/ectroudt/anaconda3/bin/python3.6"
        program = "/home/ectroudt/TCGA_Code/GDC_Data_Processing/process_salmon_SEAN.py"
        program_arg_1 = str(j)

        subprocess.Popen(["screen", "-S", scr_name, "-d", "-m", program_cmd, program, program_arg_1, "--split_Num",
                          split_num_call])


def main():

    parser = argparse.ArgumentParser(description="Retrieve current split and split number")

    # Arguments is optional, MUST be an int value between 2-6 if passed with call to 'Automate_to_Salmon.py'
    parser.add_argument("--split_Val", type=int, nargs="?", choices=range(2, 7), default=6,
                        help="Split number for # of salmon processes to be ran concurrently")

    split_Num_Arg = parser.parse_args()
    split_Val = split_Num_Arg.split_Val
    initiate_Salmon(split_Val)

    print("\n Bam files being processed by Salmon in the following screen sessions: \n")
    subprocess.call(["screen", "-ls"])


main()

