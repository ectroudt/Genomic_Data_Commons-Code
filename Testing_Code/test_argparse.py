#!/home/ectroudt/anaconda3/bin/python3.6


import argparse


def main():

    parser = argparse.ArgumentParser(description="Retrieve Location and Run info")
    parser.add_argument("man_Folder", type=str, nargs="?",
                        help="Directory location of folder containing manifest and all other relevant project files")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--whole_run", dest="run_status", action="store_true",
                       help="Determine if working on first half, or entire Manifest folder")
    group.add_argument("--first_half", dest="run_status", action="store_false",
                       help="Determine if working first half, or entire Manifest folder")
    parser.set_defaults(run_status=True)

    prog_Args = parser.parse_args()
    print(prog_Args.man_Folder)
    print(prog_Args.run_status)

main()