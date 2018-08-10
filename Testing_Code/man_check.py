with open("/home/ectroudt/test_LGG/gdc_manifest_20180313_173318.txt") as y:
 	yRead = y.readlines()
trackList = []
count = 0
for i in range(0, 6):
	with open(("/home/ectroudt/tcga_Project_Files/gdc_manifest_20180313_173318_cp" + str(i) + ".txt")) as x:
		xRead = x.readlines()			
		count += (len(xRead) - 1)
		for xLine in xRead:
			if "id" in xLine:
				pass
			
			else:
				trackList.append(str(xLine))

for yLine in yRead:
	if str(yLine) not in trackList:
		print(str(yLine))
print(count)
