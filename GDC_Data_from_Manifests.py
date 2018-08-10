#!/home/ectroudt/anaconda3/bin/python3.6

import os
import sys
import json
from GDC_Manifest_Process import process_Data, manifest_eval
from GDC_FileData import GDCprocess


def main():

    project_dir = str(sys.argv[1])

    with os.scandir(project_dir) as project_listing:

        for project in project_listing:

            project_path = project.path

            TCGA_manifest = GDCprocess(project_path)
            print("\n#################### Processing data for: " + str(TCGA_manifest.project_id) + " ####################\n")

            TCGA_manifest.file_summary()

            metadata_conv_dict = TCGA_manifest.barcodes_from_metadata()
            annot_barcodes = TCGA_manifest.barcodes_from_annot()
            deathData = TCGA_manifest.deathData_from_clin()

            case_total, death_num, bamNum, case_dict = process_Data(TCGA_manifest, metadata_conv_dict,
                                                                    annot_barcodes, deathData)

            manifest_eval(case_total, death_num, bamNum)

            cases_mult_BAMS = {}

            for case, BAMs in case_dict.items():

                if BAMs > 1:

                    cases_mult_BAMS[str(case)] = BAMs

            dataOutfile = "/home/ectroudt/TCGA_Processed_Projects_Data/" + str(TCGA_manifest.project_id) + "_data"

            with open(dataOutfile, "w") as outData:

                outData.write("###################################################################\n")
                outData.write(str(TCGA_manifest.project_id) + " Cases: \n")
                outData.write("Total Cases: " + str(len(case_dict)) + "\n\n")
                outData.write(json.dumps(case_dict))
                outData.write("\n###################################################################\n")
                outData.write(str(TCGA_manifest.project_id) + " Multi-BAM Cases:\n")
                outData.write("Total Multi-BAM Cases: " + str(len(cases_mult_BAMS)) + "\n\n")
                outData.write(json.dumps(cases_mult_BAMS))


main()

