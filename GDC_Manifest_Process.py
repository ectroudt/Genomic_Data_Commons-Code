
import os
import sys
import subprocess
from time import sleep
from contextlib import redirect_stdout
from GDC_FileData import GDCprocess


def process_Data(GDC_Object, conversion_dict, annotated_cases, clin_data):

    # ***Extract data from TCGA Project Files ***

    # Open manifest file and write ONLY those BAM files to it that do not have annotations
    new_man_file = open(GDC_Object.manifest, "w")

    # 'count' = number of Cases, 'bamCount' = number of BAM files, 'deathTracker' = number of Deaths
    id_Index = GDC_Object.man_file[0].split('\t').index('id')

    count = 0
    bamCount = 0
    deathTracker = 0
    case_data = {}

    for record in GDC_Object.man_file:

        list_record = record.split('\t')

        barcode = conversion_dict.get(list_record[id_Index], None)

        # Does the TCGA Case of this BAM file have any annotations?
        # Is there any data associated with the TCGA Case that has annotations?
        # (i.e. Any aliquots, analytes, samples, etc. from ths case)
        if barcode not in annotated_cases:

            new_man_file.write(record)

            # Is this a barcode for a case, or the Manifest header?
            if barcode is not None:

                bamCount += 1

                # Is this the first BAM file associated with this case, or does it contain multiple BAM files?
                if case_data.get(str(barcode), None) is None:

                    case_data[str(barcode)] = 1

                    count += 1

                    # Did the Patient for this Case die?
                    if clin_data.get(barcode) is not None:

                        deathTracker += 1

                else:

                    case_data[str(barcode)] += 1

    new_man_file.close()

    return count, deathTracker, bamCount, case_data


def manifest_eval(data_count, death_count, bamTotal, survivalCutoff=25):

    if data_count == 0:

        survivalPerc = 0

        print("All cases were annotated...\n")

    else:

        survivalPerc = round(((death_count/data_count)*100), 1)

        print("Manifest File now contains " + str(bamTotal) + " BAM files, and " + str(data_count) +
              " cases, of which " + str(survivalPerc) + "% have died \n")

    if survivalPerc < survivalCutoff:

        print("Number of patients that have died does not exceed " + str(survivalCutoff) + "%....\n")

        return False

    else:

        return True


def project_Analysis(GDC_Object, first_run_status, split_Val):

    proceed = True

    if first_run_status:

        # Obtain the corresponding Project data (Project Cases are referred to as 'barcodes')
        metadata_conv_dict = GDC_Object.barcodes_from_metadata()
        annot_barcodes = GDC_Object.barcodes_from_annot()
        deathData = GDC_Object.deathData_from_clin()

        caseTotal, death_num, bamTotal, cases = process_Data(GDC_Object, metadata_conv_dict, annot_barcodes, deathData)

        # Does the Number of deaths exceed 25%?
        if manifest_eval(caseTotal, death_num, bamTotal):

            # Is the Manifest folder small enough to download all BAM files at once?
            if bamTotal <= 230:

                # run gdc-client to download ALL BAM files
                download_manifest(GDC_Object, split_num=split_Val)

            else:

                download_manifest(GDC_Object, entire_Man_Folder=False, split_num=split_Val)

        else:

            proceed = False

        return proceed

    else:

        print("\n******Initiating gdc-client for download of second half of manifest files for: "
              + str(GDC_Object.project_id) + "******\n\n")

        download_manifest(GDC_Object, entire_Man_Folder=False, first_run=False, split_num=split_Val)

        return proceed


def download_manifest(GDC_Object, entire_Man_Folder=True, first_run=True, split_num=6):

    # Make sure gdc-client auth key has permissions modified (600) so only owner can read and write
    # Subprocess Popen with screen seems to terminate if any warning messages appear when running gdc-client

    program = "/usr/local/bin/gdc-client"
    program_key = "******************"

    if first_run:

        out_dir = str(create_dir(GDC_Object)[0])

    else:

        out_dir = str(create_dir(GDC_Object, obtain_only=True)[0])

    for j in range(0, split_num):
        scr_name = "gdcMan_DownloadScreen_" + str(j)
        program_arg = extract_manifest_portion(GDC_Object, split_num, j, entire_Man_Folder, first_run)

        subprocess.Popen(["screen", "-S", scr_name, "-d", "-m", program, "download", "-m", program_arg, "-t",
                          program_key], cwd=out_dir)

    print("\n Manifest folder downloading in the following screen sessions: \n")
    subprocess.call(["screen", "-ls"])


def create_dir(GDC_Object, obtain_only=False):

    # ***Create and obtain directories for Project download and abundance files***

    download_directory = "/data/rnaSeq/TCGA_Projects/" + GDC_Object.project_id + "/" + GDC_Object.project_name\
                         + "_download_files"
    abundance_directory = "/data/rnaSeq/TCGA_Projects/" + GDC_Object.project_id + "/" + GDC_Object.project_name\
                          + "_Abundances"

    if not obtain_only:

        os.makedirs(download_directory)
        os.makedirs(abundance_directory)

    return [download_directory, abundance_directory]


def extract_manifest_portion(GDC_Object, split_num, current_split, entire_Manifest=True, first_run=True):

    # ***Create separate individual manifest files that contain corresponding portion of BAM files***
    # i.e. when 'split_num' = 6, and 'current_split' = 2, return Manifest file of 2nd portion (out of 6)

    with open(GDC_Object.manifest) as master_manifest:

        master_manifest = master_manifest.readlines()
        man_header = str(master_manifest[0])
        man_Length = int((len(master_manifest) - 1))
        man_Range = int(man_Length / (split_num - 1))

    # How many BAM files will a portion contain?
    if not entire_Manifest:

        man_Range = int(man_Range / 2)
        man_Length = int(man_Length / 2)

        if first_run:

            master_manifest = master_manifest[:man_Length]

        else:

            master_manifest = master_manifest[man_Length:]

    manifest_portion = str(GDC_Object.manifest) + "_cp" + str(current_split)

    with open(manifest_portion, "w") as man_portion:

        # Does this portion contain the Manifest header?
        if current_split != 0 or not first_run:

            # Make sure Manifest header is included for each Manifest file
            # Otherwise gdc-client will not run
            man_portion.write(man_header)

        start = int(current_split * man_Range)
        end = int((current_split + 1) * man_Range)

        for case in master_manifest[start:end]:
            man_portion.write(str(case))

    return manifest_portion


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
    filename = file_dir + str(project_Name)

    with open(filename, "a") as outfile:

        with redirect_stdout(outfile):

            print("\n\n******************Salmon processing******************\n\n")

            print("salmon processes are starting from screen session:  \n")

            subprocess.call(["screen", "-ls"], stdout=outfile)


def main():

    # System argument MUST contain absolute path of TCGA-Project folder
    tcga_project_files = sys.argv[1]

    first_run_status = ((sys.argv[2]) == "True")

    split_Val = int(sys.argv[3])

    TCGA_manifest = GDCprocess(tcga_project_files)
    TCGA_manifest.file_summary()

    if project_Analysis(TCGA_manifest, first_run_status, split_Val):

        # monitor progress of gdc-client until it's finished
        process_Control(TCGA_manifest.project_id)

        # run salmon on downloaded BAM files
        run_Salmon(TCGA_manifest.project_id, split_Val)


if __name__ == '__main__':

    main()

