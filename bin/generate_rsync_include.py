#!/usr/bin/python

import sys
sys.path.append('.')
import argparse

from vacker.media_collection import AllMedia


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--output', '-o', type=str, dest='output_file',
                    help='Output file for rsync', required=True)
parser.add_argument('--strip-path', '-s', type=str, dest='strip_path',
                    help=('Path to strip from start of lines - '
                          'Useful for relative rsync commands'))

args = parser.parse_args()

collection = AllMedia()
# Need to obtain from arguments
output = collection.get_backup_media_paths(args.strip_path)
with open(args.output_file, 'w') as fh:
    fh.write(output)
