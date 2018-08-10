import os
import sys
import re
import json


class GDCprocess(object):

    # Path for tcga_Dir MUST BE absolute path, or Popen will not run

    def __init__(self, tcga_Dir):

        # Create variables for all project files
        self.project_files = os.listdir(tcga_Dir)
        self.manifest, self.metadata, self.annot, self.clin = None, None, None, None
        self.man_file, self.annot_cases, self.meta_cases, self.clin_cases = None, None, None, None

        # Get rid of / at end
        self.test_char = str(tcga_Dir)[-1]

        if self.test_char == "/":
            tcga_Dir = str(tcga_Dir[:-1])

        # Extract project id and project name from system argument for project directory
        # MUST EDIT CODE IF DIRECTORIES ARE CHANGED
        self.project_id = str(tcga_Dir[tcga_Dir.index("i") + 4:])
        self.project_name = str(self.project_id[(self.project_id.index("-") + 1):])

        # Organize files and extract data needed from them
        self.projectFile_assignment(tcga_Dir)
        self.access_project_files()

    # Organize files from Project directory
    def projectFile_assignment(self, tcga_Dir):

        for self.datafile in self.project_files:

            if re.search(r'^gdc_man', str(self.datafile)):

                self.manifest = str(tcga_Dir) + "/" + str(self.datafile)

            elif re.search(r'^metadata.*json$', str(self.datafile)):

                self.metadata = str(tcga_Dir) + "/" + str(self.datafile)

            elif re.search(r'^clin.*json$', str(self.datafile)):

                self.clin = str(tcga_Dir) + "/" + str(self.datafile)

            elif re.search(r'^annot.*json$', str(self.datafile)):

                self.annot = str(tcga_Dir) + "/" + str(self.datafile)

    # Open and extract data from each file
    def access_project_files(self):

        if len(self.project_files) != 4:

            print("File directory does not contain correct number of files")
            sys.exit()

        try:

            with open(self.manifest) as self.manifest_data:
                self.man_file = self.manifest_data.readlines()

                for self.man_line in self.man_file:
                    self.man_line.rstrip("\n")

            with open(self.annot) as self.annot_file:
                self.annot_cases = json.load(self.annot_file)
                self.annot_cases = self.annot_cases["data"]["hits"]

            with open(self.metadata) as self.meta_file:
                self.meta_cases = json.load(self.meta_file)
                self.meta_cases = self.meta_cases["data"]["hits"]

            with open(self.clin) as self.clin_file:
                self.clin_cases = json.load(self.clin_file)
                self.clin_cases = self.clin_cases["data"]["hits"]

        except TypeError as bad_file:

            print("\n A project file is an incorrect type >> " + str(bad_file.args[0]) + "\n")
            print("Check ~/tcga_Project_Files to make sure it has correct files...\n")
            sys.exit()

        except IOError as bad_file:

            print("\nThere is a file input/output error >> " + str(bad_file.args[1] + "\n"))
            print("Check ~/tcga_Project_Files...\n")
            sys.exit()

        except Exception as prob:

            print("\n A File from the directory is bad >> " + str(prob.args[0]) + "\n")
            sys.exit()

    # Print information about contents on each project file
    def file_summary(self):

        print("\nProject ID: " + str(self.project_id) + "\n")
        print("Project name: " + str(self.project_name) + "\n")
        print("\n**The manifest file contains " + str((len(self.man_file) - 1)) + " BAM files, at file path: " +
              str(self.manifest) + "\n")
        print("**The metadata file contains " + str(len(self.meta_cases)) + " data items" + "\n")
        print("**The annotations file contains " + str(len(self.annot_cases)) + " cases" + "\n")
        print("**The clinical file contains " + str(len(self.clin_cases)) + " cases" + "\n")

    # Create dict of uuids and their associated barcodes
    def barcodes_from_metadata(self):

        self.uuid_barcode_conv = {}

        for self.case in self.meta_cases:

            self.uuid_key = str(self.case.get('file_id'))

            for self.record in self.case.get('associated_entities'):

                self.caseBarcode = str(self.record['entity_submitter_id'][:12])

                self.uuid_barcode_conv[self.uuid_key] = self.caseBarcode

        return self.uuid_barcode_conv

    # Obtain all barcodes present in annotation file
    def barcodes_from_annot(self):

        return [self.case.get('case_submitter_id') for self.case in self.annot_cases]

    # Obtain the days to death for each individual in clinical file
    def deathData_from_clin(self):

        self.barcode_to_death_status = {}

        for self.ind_Case in self.clin_cases:

            if self.ind_Case.get("diagnoses") is not None:

                self.diagData = self.ind_Case.get("diagnoses")[0]
                self.barcode = str(self.diagData.get("submitter_id")[:12])
                self.dtd = self.diagData.get("days_to_death")

                if (self.dtd is None) and (self.diagData.get("vital_status") == "dead"):
                    self.dtd = "dead"

                self.barcode_to_death_status[self.barcode] = self.dtd

        return self.barcode_to_death_status








