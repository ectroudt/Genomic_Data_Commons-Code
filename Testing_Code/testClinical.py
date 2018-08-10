import json


import sys



with open(sys.argv[1]) as clin_file:

    jUnp = json.load(clin_file)
    jUnp = jUnp["data"]["hits"]
    count = 0
    trackDeath = 0
    trackDeath2 = 0
    print(str(len(jUnp)))

    for ind_Case in jUnp:

        if ind_Case.get("diagnoses") is not None:

            diagData = ind_Case.get("diagnoses")[0]
            print(diagData)

            barcode = str(diagData.get("submitter_id"))
            print(barcode)

            dtd = diagData.get("days_to_death")
            print(dtd)

            if diagData.get("vital_status") == "dead":
                trackDeath2 += 1

            if dtd is not None:
                trackDeath += 1

            if (diagData.get("vital_status") == "dead") and (dtd is None):

                dtd = "dead"
                trackDeath += 1
            count += 1




    print(str(count) + " cases, " + str(trackDeath) + " patients died")
    print(str(trackDeath2))

