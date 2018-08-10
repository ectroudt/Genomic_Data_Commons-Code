#!/home/ectroudt/anaconda3/bin/python3.6

import requests
import sys
import os


def obtain_Manifest(project_id_name, filter_dict=None):

    project_id = project_id_name
    project_file_name = "gdc_man_" + str(project_id)

    files_endpt = "https://api.gdc.cancer.gov/files"

    params = {
        "filters": filter_dict,
        "size": "2000",
        "return_type": "manifest"
    }

    response = requests.post(files_endpt, headers={"Content-Type": "application/json"}, json=params)

    with open("/home/ectroudt/TCGA_Processed_Dirs/" + str(project_id) + "/" + str(project_file_name), "w") as manFile:
        manFile.write(response.content.decode("utf-8"))


def obtain_Metadata(project_id_name, filter_dict=None):

    project_id = project_id_name
    project_file_name = "metadata" + str(project_id) + str(".json")

    files_endpt = "https://api.gdc.cancer.gov/files"

    params = {
        "filters": filter_dict,
        "fields": "file_id",
        "expand": "associated_entities",
        "size": "2000",
    }

    response = requests.post(files_endpt, headers={"Content-Type": "application/json"}, json=params)

    with open("/home/ectroudt/TCGA_Processed_Dirs/" + str(project_id) + "/" + str(project_file_name), "w") as metaFile:
        metaFile.write(response.content.decode("utf-8"))


def obtain_Clindata(project_id_name, filter_dict=None):

    project_id = project_id_name
    project_file_name = "clinical_" + str(project_id) + str(".json")

    files_endpt = "https://api.gdc.cancer.gov/cases"

    params = {
        "filters": filter_dict,
        "fields": "diagnoses.submitter_id,diagnoses.days_to_death,diagnoses.vital_status",
        "size": "2000"
    }

    response = requests.post(files_endpt, headers={"Content-Type": "application/json"}, json=params)

    with open("/home/ectroudt/TCGA_Processed_Dirs/" + str(project_id) + "/" + str(project_file_name), "w") as clinFile:
        clinFile.write(response.content.decode("utf-8"))


def obtain_Annotdata(project_id_name, filter_dict=None):

    project_id = project_id_name
    project_file_name = "annot" + str(project_id) + ".json"

    files_endpt = "https://api.gdc.cancer.gov/annotations"

    filters = {"op": "in",
               "content": {
                   "field": "project.project_id",
                   "value": [project_id]}
               }

    params = {
        "filters": filters,
        "size": "2000",
        "fields": "case_submitter_id,project.project_id"
    }

    response = requests.post(files_endpt, headers={"Content-Type": "application/json"}, json=params)

    with open("/home/ectroudt/TCGA_Processed_Dirs/" + str(project_id) + "/" + str(project_file_name), "w") as annotFile:
        annotFile.write(response.content.decode("utf-8"))


def main():

    project_id = str(sys.argv[1])
    os.mkdir("/home/ectroudt/TCGA_Processed_Dirs/" + str(project_id))


    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": [project_id]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.experimental_strategy",
                    "value": ["RNA-Seq"]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.data_format",
                    "value": ["BAM"]
                }
            }
        ]
    }

    try:

        obtain_Manifest(project_id, filters)
        obtain_Metadata(project_id, filters)
        obtain_Annotdata(project_id)
        obtain_Clindata(project_id, filters)

    except requests.HTTPError as http_prob:

        print("\nHTTP Error occurred: " + str(http_prob) + "\n\n")
        sys.exit()

    except requests.RequestException as prob:
        print("\nProblem with requests: " + str(prob.response) + "\n\n")


main()

