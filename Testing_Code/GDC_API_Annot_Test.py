#!/home/ectroudt/anaconda3/bin/python3.6

import requests
import sys

project_id = str(sys.argv[1])
project_file_name = "annot" + str(project_id) + ".json"


files_endpt = "https://api.gdc.cancer.gov/annotations"

# This set of filters is nested under an 'and' operator.
filters = {"op": "in",
           "content": {
                "field": "project.project_id",
                "value": [project_id]
                }
           }



# A POST is used, so the filter parameters can be passed directly as a Dict object.
params = {
    "filters": filters,
    "size": "2000",
    "fields": "case_submitter_id"
    }

# The parameters are passed to 'json' rather than 'params' in this case
response = requests.post(files_endpt, headers = {"Content-Type": "application/json"}, json = params)


with open("/home/ectroudt/tcga_Project_Files/" + str(project_id) + "/" + str(project_file_name), "w") as annotFile:

    annotFile.write(response.content.decode("utf-8"))