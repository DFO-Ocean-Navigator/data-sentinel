#!/usr/bin/env python
import argparse
import json
import re
import sys

import xarray as xr


def create_parser():
    parser = argparse.ArgumentParser(prog='Data Sentinel',
                                     description='Detect differences in metadata in netcdf files.')

    parser.add_argument('incoming', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin, help='Path or stdin to files to be checked.')
    parser.add_argument('--dataset', type=str, required=True,
                        help='Dataset key to be tested that is in template file (e.g. giops_daily).')
    parser.add_argument(
        '--template', type=argparse.FileType('r'), required=True, help='Path to template file.')

    return parser


def read_json(file):
    return json.load(file)


def read_file(file):
    return [line.rstrip('\n') for line in file]


def check_files(template_dict, incoming_files):

    for p in template_dict.keys():
        regex = re.compile(p)

        matched = filter(regex.search, incoming_files)
        if not matched:
            print("No files matched with the regex " + p)
            continue

        known_file = template_dict[p]
        with xr.open_dataset(known_file) as known_dataset:

            for f in matched:
                #todo need full path for file
                print(f)


    return True


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    print("Reading template...")
    data = read_json(args.template)

    dataset = args.dataset
    print("Ingesting incoming files...")
    incoming_files = read_file(args.incoming)

    print("Checking files...")
    check_files(data[dataset], incoming_files)
