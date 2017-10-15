#!/usr/bin/python

import sys
sys.path.append('.')
import argparse

from vacker.importer import Importer


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--directory', '-d', type=str, dest='directory',
                    help='Directory to import', required=True)

args = parser.parse_args()



importer = Importer()
# Need to obtain from arguments
importer.import_directory(args.directory)
