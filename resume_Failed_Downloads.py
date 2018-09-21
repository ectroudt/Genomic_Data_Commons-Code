#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import subprocess
from time import sleep
from contextlib import redirect_stdout


def process_Control(project_Name):

    sleep(120)

    download_status = process_Check()

    elapse_time = 2
    file_dir = "/home/ectroudt/gdc_download_logs/"
    filename = file_dir + str(project_Name)

    # While current gdc-client processes are running...
    while download_status:

        # Wait two hours and check again
        sleep(7200)

        # Document the timeframe of downloadin the BAM files in a log file
        with open(filename, "a") as outfile:

            with redirect_stdout(outfile):

                print("Checking if gdc-client processes are still running.." + "\n" + "elapsed time: "
                      + str(elapse_time) + " hours")

        elapse_time += 2

        download_status = process_Check()


def process_Check():

    # **Check the current processes running for ectroudt and determine if any gdc-client processes remain

    procs = subprocess.check_output(["ps", "-u", "ectroudt"])
    procs = procs.decode("UTF-8")

    return "gdc-client" in str(procs)


def run_Salmon(project_Name, split_num):

    # split_num is set to 6 by default, unless different argument is passed
    split_num_call = str(split_num)

    for j in range(1, (split_num + 1)):

        scr_name = "salmon_processing_" + str(j)
        program_cmd = "/home/ectroudt/anaconda3/bin/python3.6"
        program = "/home/ectroudt/TCGA_Code/GDC_Data_Processing/process_salmon_SEAN.py"
        program_arg_1 = str(j)

        subprocess.Popen(["screen", "-S", scr_name, "-d", "-m", program_cmd, program, program_arg_1, "--split_Num",
                          split_num_call])

    file_dir = "/home/ectroudt/gdc_download_logs/"
    filename = file_dir + str(project_Name) + "_salmon"

    with open(filename, "a") as outfile:

        with redirect_stdout(outfile):

            subprocess.call(["screen", "-ls"], stdout=outfile)


def main():

    project_Name = str(sys.argv[1])

    process_Control(project_Name)

    run_Salmon(project_Name, split_num=6)


if __name__ == '__main__':

    main()