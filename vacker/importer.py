
import os
import datetime
from mimetypes import MimeTypes
import uuid

import vacker.analyser
import vacker.analyser.factory
import vacker.file_factory
import vacker.database
import vacker.config


class Importer(object):

    def __init__(self):
        self.analyser_factory = vacker.analyser.factory.Factory
        self.file_factory = vacker.file_factory.FileFactory()
        self.database = vacker.database.Database()

    def import_directory(self, directory, verify=False):
        # Walk down each directory, getting all files in each directory
        for root, _, files in os.walk(directory):
            # Iterate over files and...
            for file in files:
                # Import each one
                print('Importing ' + file)
                self.import_file(os.path.join(root, file), verify=verify)

        self.database.complete_batch()

    def import_file(self, file_path, verify):
        # Determine file type

        # Only continue if:
        #  - File does not already exist in DB
        #  - Files already exists, verify has been passed and the actual file is not the same as DB
        existing_file = self.file_factory.get_file_by_path(file_path)
        if existing_file and (not verify or self.file_factory.compare_file(file_path)):
            return False

        file_obj = self.analyser_factory.analyse_file(file_path)
        print(file_obj.properties)
        self.database.insert_batch(file_obj.properties)
