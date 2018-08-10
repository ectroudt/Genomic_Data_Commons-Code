import os

indirname = ""
preprefix = ""


for project_folder in os.listdir("/data/rnaSeq/TCGA_Projects/"):

    if "TCGA" in str(project_folder):

        project_Dir = os.path.join("/data/rnaSeq/TCGA_Projects/", project_folder)

        for data_Dir in os.listdir(project_Dir):

            if "download" in str(data_Dir):

                indirname = os.path.join(project_Dir, data_Dir) + "/"

            else:

                preprefix = os.path.join(project_Dir, data_Dir) + "/"

print("Download Directory: " + str(indirname))
print("Abundance Directory: " + str(preprefix))