#!/usr/bin/python

import sys
sys.path.append('.')

from vacker.importer import Importer

importer = Importer()
# Need to obtain from arguments
importer.import_directory('../sample_photos')
