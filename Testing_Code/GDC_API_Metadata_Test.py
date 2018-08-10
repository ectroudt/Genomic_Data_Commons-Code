#!/home/ectroudt/anaconda3/bin/python3.6

import requests
import sys
import os

project_id = str(sys.argv[1])
project_file_name = "metadata" + str(project_id) + str(".json")


files_endpt = "https://api.gdc.cancer.gov/files"

# This set of filters is nested under an 'and' operator.
filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "cases.project.project_id",
            "value": [project_id]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "files.experimental_strategy",
            "value": ["RNA-Seq"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "files.data_format",
            "value": ["BAM"]
            }
        }
    ]
}

# A POST is used, so the filter parameters can be passed directly as a Dict object.
params = {
    "filters": filters,
    "fields": "file_id",
    "expand": "associated_entities",
    "size": "2000",
    }

# The parameters are passed to 'json' rather than 'params' in this case
response = requests.post(files_endpt, headers = {"Content-Type": "application/json"}, json = params)


with open("/home/ectroudt/tcga_Project_Files/" + str(project_id) + "/" + str(project_file_name), "w") as metaFile:

    metaFile.write(response.content.decode("utf-8"))