#!/usr/bin/env python
import argparse
import json
import re
import sys

import xarray as xr

from pretty_print import bcolors
from rules import check_rules
from template import Template


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


def check_files(template, incoming_files):

    passed = []
    failed = []
    for pattern, filename in template.known_files.items():
        regex = re.compile(pattern)

        matched = filter(regex.search, incoming_files)
        if not matched:
            print("No files matched with the regex %s." % pattern)
            continue

        with xr.open_dataset(filename) as known_dataset:
            for f in matched:
                with xr.open_dataset(f) as spooky_dataset:
                    if(check_rules(template.rules, known_dataset, spooky_dataset)):
                        passed.append(f)
                    else:
                        failed.append(f)

    return passed, failed


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    dataset = args.dataset

    print(bcolors.HEADER + "Reading template..." + bcolors.ENDC)
    template = Template(read_json(args.template)[dataset])

    print(bcolors.HEADER + "Ingesting incoming files..." + bcolors.ENDC)
    incoming_files = read_file(args.incoming)

    print(bcolors.HEADER + "Checking files..." + bcolors.ENDC)
    passed, failed = check_files(template, incoming_files)

    print(bcolors.HEADER + "Results..." + bcolors.ENDC)
    print(bcolors.OKGREEN + "%d files passed." % len(passed) + bcolors.ENDC)
    print(bcolors.FAIL + "%d files failed." % len(failed) + bcolors.ENDC)
