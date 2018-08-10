#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import json

with open(str(sys.argv[1])) as metaFile:

    metadata = json.load(metaFile)
    metadata = metadata["data"]["hits"]

print(len(metadata))
print(str(metadata[0]))
count = 0

for item in metadata:
    print(str(item.get('file_id')))

    for vals in item.get('associated_entities'):
        print(str(vals['entity_submitter_id'][:12]))
        print(str(vals['entity_submitter_id']))

        if str(vals['entity_type']) == 'aliquot':

            count += 1

print(count)