#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import json

with open(str(sys.argv[1])) as annotFile:

    annotData = json.load(annotFile)
    annotData = annotData["data"]["hits"]


print(len(annotData))

if len(annotData) is not 0:

    for item in annotData:
        print(str(item))
else:
    print("Error")