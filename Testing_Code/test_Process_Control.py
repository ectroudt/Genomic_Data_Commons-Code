#!/home/ectroudt/anaconda3/bin/python3.6

import subprocess
import psutil
from time import sleep
from contextlib import redirect_stdout
import datetime


def process_Control():

    procs = [psutil.Process(p.info['pid']) for p in psutil.process_iter(attrs=['pid', 'name', 'username'])]

    for spec_proc in procs:
        print(str(spec_proc.name()) + " *** " + str(spec_proc.status()) + " *** " + str(spec_proc.cmdline()))
        created = datetime.datetime.fromtimestamp(spec_proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        print("Created ---> " + str(created) + "\n")

        for cProc in spec_proc.children():
            print("\tCHILD PROCESSES: ")
            print("\t" + str(cProc.name()) + " *** " + str(cProc.status()) + " *** " + str(cProc.cmdline()))
            created = datetime.datetime.fromtimestamp(cProc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            print("\t" + "Created ---> " + str(created) + "\n")

        print("\n")

def main():

    print("Process beginning...")

    program = "/usr/local/bin/gdc-client"
    program_key = "/home/ectroudt/gdc-user-token.2018-05-17T20_50_21.281Z.txt"
    out_dir = "/home/ectroudt/TCGA_Project_Test_Data"

    scr_name = "gdcMan_Download"
    program_arg = "/home/ectroudt/TCGA_Project_Test_Data/gdc_man_TCGA-ESCA_cp5"

    subprocess.Popen(["screen", "-S", scr_name, "-d", "-m", program, "download", "-m", program_arg, "-t", program_key],
                     cwd=out_dir)

    current_salmon_Procs = process_Control()
    elapse_time = 0
    while current_salmon_Procs:

        sleep(60)
        file_dir = "/home/ectroudt/gdc_download_logs/"
        filename = file_dir + "test"

        with open(filename, "a") as outfile:
            with redirect_stdout(outfile):
                print("Checking if gdc-client processes are still running.." + "\n" + "elapsed time: "
                      + str(elapse_time) + " hours")

        elapse_time += 2
        current_salmon_Procs = process_Control()

    print("Process complete")

if __name__ == '__main__':
    main()