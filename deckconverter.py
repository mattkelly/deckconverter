#!/usr/bin/python
import argparse

def parse_args():
    desc = "A utility for converting between card deck formats"

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source_file", action="store", help="The original file")
    parser.add_argument("destination_file", action="store", help="The file that will be created")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
