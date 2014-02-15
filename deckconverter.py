#!/usr/bin/python
import sys
import argparse

def parse_args():
    desc = "A utility for converting between card deck formats"

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source_file", action="store", help="The original file")
    parser.add_argument("destination_file", action="store", help="The file that will be created")

    args = parser.parse_args()
    return args

def overwrite_prompt(filename):
    invalid = True
    while invalid:
        sys.stdout.write(filename + " exists!. Do you want to overwrite it? [y/n]")
        choice = raw_input().lower()[:1]
        if choice == "y" or choice == "n":
            invalid = False
        
    return choice == "y"

if __name__ == "__main__":
    args = parse_args()

    try:
        with open(args.destination_file):
            overwrite = overwrite_prompt(args.destination_file)
            if overwrite:
                convert_deck(args.source_file, args.destination_file)
            else:
                sys.stderr.write(args.destination_file + " will not be overwritten! Exiting ...")
                sys.exit(1)
    except IOError:
        convert_deck(args.source_file, args.destination_file)
