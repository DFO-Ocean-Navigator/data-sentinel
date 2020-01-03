#!/usr/bin/env python
import argparse
import json
import sys
import netcdf4


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


def check_files(template_dict, incoming_files):
    return True


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    data = read_json(args.template)

    dataset = args.dataset
    incoming_files = args.incoming

    check_files(data[dataset], incoming_files)
