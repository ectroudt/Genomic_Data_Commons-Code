#!/home/ectroudt/anaconda3/bin/python3.6

import sys
import os

def main():

    project_dir = str(sys.argv[1])

    with os.scandir(project_dir) as project_listing:

        for project in project_listing:

            project_path = project.path

            print(str(project_path))


main()