
def command_Mod(testing=False):

    if testing:

        pass

    else:

        with open("/home/ectroudt/TCGA_Code/GDC_Data_Processing/check_Downloads") as x:

            download_Pro = x.readlines()

        with open("/home/ectroudt/TCGA_Code/GDC_Data_Processing/check_Downloads", "w") as w:

            for fileline in download_Pro:

                if "os.listdir" in fileline:

                    w.write("print(len(os.listdir(" + str(download_dir) + ")))")

                else:

                    w.write(str(fileline))

        with open("/home/ectroudt/TCGA_Code/GDC_Data_Processing/check_Project_Data") as x:

            download_Pro = x.readlines()

        with open("/home/ectroudt/TCGA_Code/GDC_Data_Processing/check_Project_Data", "w") as w:

            for fileline in download_Pro:

                if "os.listdir" in fileline:

                    w.write("print(len(os.listdir(" + str(abundance_dir) + ")))")

                else:

                    w.write(str(fileline))