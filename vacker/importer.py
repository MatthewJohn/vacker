
import os
import datetime
from mimetypes import MimeTypes
import uuid

import vacker.analyser
import vacker.analyser.factory
import vacker.analyser.file
import vacker.file_factory
import vacker.database
import vacker.config


class Importer(object):

    def __init__(self):
        self.analyser_factory = vacker.analyser.factory.Factory
        self.file_factory = vacker.file_factory.FileFactory()
        self.database = vacker.database.Database()

    def import_directory(self, directory, verify=False, skip=None):
        # Walk down each directory, getting all files in each directory
        dirs_to_skip, files_to_skip = skip.split(',') if skip else (0, 0)
        dirs_to_skip = int(dirs_to_skip)
        files_to_skip = int(files_to_skip)
        skip_dir = 0
        skip_file = 0
        for root, _, files in os.walk(directory):
            if dirs_to_skip:
                skip_dir += 1
                dirs_to_skip -= 1
                continue

            # Iterate over files and..i.
            for file in files:
                if files_to_skip:
                    skip_file += 1
                    files_to_skip -= 1
                    continue

                # Import each one
                print('Importing ' + file)
                try:
                    self.import_file(os.path.join(root, file), verify=verify)
                except:
                    try:
                        self.database.complete_batch()
                    except:
                        print('WARNING: Unable to commit final batch')
                    print('To continue, use argument --skip=' + str(skip_dir) + ',' + str(skip_file))
                    raise
                skip_file += 1
            skip_file = 0
            skip_dir += 1

        self.database.complete_batch()

    def import_file(self, file_path, verify):
        # Determine file type

        # Only continue if:
        #  - File does not already exist in DB
        #  - Files already exists, verify has been passed and the actual file is not the same as DB
        existing_file = self.file_factory.get_file_by_path(file_path)
        if existing_file and (not verify or self.file_factory.compare_file(file_path)):
            return False

        file_objs = self.analyser_factory.analyse_file(
            vacker.analyser.file.File(file_path))
        for file_obj in file_objs:
            print(file_obj.properties)
            self.database.insert_batch(file_obj.properties)
