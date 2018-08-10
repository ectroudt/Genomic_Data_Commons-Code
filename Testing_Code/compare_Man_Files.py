import sys

with open(sys.argv[1]) as API_Man:

    API_Vers = API_Man.readlines()

with open(sys.argv[2]) as regular_Man:

    regular_Vers = regular_Man.readlines()

count = 0

APImanifest = []
regularmanifest = []

for i in API_Vers:

    APImanifest.append(str(i.rstrip("\n")))


for l in regular_Vers:

    regularmanifest.append(str(l.rstrip("\n")))

print("APIManifest = " + str(len(APImanifest)))
print("RegularManifest = " + str(len(regularmanifest)))

for val in regularmanifest:

    if val not in APImanifest:

        print(val)
        count += 1

print(count)

count2 = 0


for APIval in APImanifest:

    if APIval not in regularmanifest:

        print(APIval)
        count2 += 1

print(count2)
