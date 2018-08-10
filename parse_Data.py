import sys
import json
import os

with open(sys.argv[1]) as x:

    cases = json.load(x)

    pro_id = str((cases[0].get("project")["project_id"]))
    project_name = (pro_id[(pro_id.index("-") + 1):])
    print(project_name)

    os.makedirs("/home/ectroudt/" + pro_id + "/" + project_name + "_download_files")