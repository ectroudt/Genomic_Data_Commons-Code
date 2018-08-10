import sys

GBM_Downloaded = open(sys.argv[1]).readlines()

processGBM = []
for line in GBM_Downloaded:
    processGBM.append(str(line).rstrip('\n'))

GBM_Man = open(sys.argv[2]).readlines()
GBM_new_Man = open(sys.argv[2], "w")

for manfile in GBM_Man:

    manifestData = manfile.split('\t')

    if str(manifestData[0]) in processGBM:

        print(str(manifestData[0]) + " Detected")

    else:

        GBM_new_Man.write(str(manfile))

GBM_new_Man.close()

