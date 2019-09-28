#!/usr/bin/python

import sys
sys.path.append('.')
import argparse

from vacker.importer import Importer


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--verify', '-v', dest='verify', default=False,
                    help='Verify files based on checksums', action='store_true')
parser.add_argument('directories', type=str,
                    help='Directory to import', nargs='+')

args = parser.parse_args()



importer = Importer()
# Need to obtain from arguments
for directory in args.directories:
    importer.import_directory(directory, verify=args.verify)
