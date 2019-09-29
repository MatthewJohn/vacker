
import os
import datetime
from mimetypes import MimeTypes
import uuid

import vacker.analyser
import vacker.file_factory
import vacker.database
import vacker.config


class Importer(object):

    def __init__(self):
        self.analyser = vacker.analyser.Analyser()
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

    def import_file(self, file, verify):
        # Determine file type
        file_type = self.analyser.detect_media_type(file)

        # Only continue if:
        #  - File does not already exist in DB
        #  - Files already exists, verify has been passed and the actual file is not the same as DB
        existing_file = self.file_factory.get_file_by_path(file)
        if existing_file and (not verify or self.file_factory.compare_file(file)):
            return False

        # Determine the type of file, and perform import depending on type
        if file_type is vacker.analyser.MediaType.PHOTO:
            try:
                # Import photo object
                media_obj = self.import_photo(file)
            except:
                return

            # If no media object exists, something went wrong, so return early
            if not media_obj:
                return False
            try:
                # Create thumbnail for image
                media_obj.create_thumbnail()
            except:
                media_obj.delete()
                return
            # Update the sets that the photo are in
            media_obj.update_sets()
            # Update any events that the photo are in
            # DISABLED as new web interface does not use it
            #media_obj.update_events()
        elif file_type is vacker.analyser.MediaType.VIDEO:
            # Import video object
            media_obj = self.import_video(file)

        else:
            media_obj = self.import_generic(file)

        # If all succeceded, return Media Object.
        return media_obj

    def import_generic(self, file_):
        """Exctract file information and import into solr"""
        file_data = {
            'id': uuid.uuid4(),
            'size': int(os.path.getsize(file_)),
            'path': file_,
            'file_name': file_.split('/')[-1],
            'directory': '/'.join(file_.split('/')[0:-1]),
            'mime_type': MimeTypes().guess_type(file_)[0]
        }
        file_data['sha1'], file_data['sha512'] = self.analyser.get_checksums(
            file_)
        file_data['extension'] = (file_data['file_name'].split('.')[-1]
                                  if '.' in file_data['file_name'] else '')

        self.database.insert_batch(file_data)


    def import_photo(self, photo):

        # Obtain image meta data
        analysed_info = self.analyser.get_image_data(photo)

        # Check is image is smaller than minimum resolution
        if (analysed_info['height'] * analysed_info['width']) < vacker.config.Config.get('MINIMUM_RESOLUTION'):
            return None

        # Obtain and add file checksum to image info
        analysed_info['checksum'] = self.analyser.get_checksum(photo)

        # Check if photo is a duplicate
        file_factory = vacker.file_factory.MediaFactory()
        dupe_media = file_factory.get_media_by_checksum(analysed_info['checksum'])
        if dupe_media:
            return None

        # Get filesystem information for additional information
        analysed_info['path'] = photo
        analysed_info['mtime'] = datetime.datetime.fromtimestamp(os.stat(photo).st_mtime)

        # Set initial null value for set and event IDs, as these will be determined later.
        analysed_info['set_id'] = None
        analysed_info['event_id'] = None

        # Set initial false value for backing up
        analysed_info['backup'] = False

        # Set initial false value for backing up
        analysed_info['hide'] = False

        # Set rating to null, as photo has not yet been rated
        analysed_info['rating'] = None

        # If the datetime has been obtained from the meta information,
        # split the year, month and day out for easier searching/indexing
        if 'datetime' in analysed_info and analysed_info['datetime']:
            analysed_info['y'] = analysed_info['datetime'].year
            analysed_info['m'] = analysed_info['datetime'].month
            analysed_info['d'] = analysed_info['datetime'].day

        # Inset into database, create Photo object and return
        photo_id = self.database.get_database().media.insert_one(analysed_info).inserted_id
        return vacker.media.photo.Photo(photo_id)

    def import_video(self, video):
        # Sorry, don't support videos YET
        print('you got vidz bro?')
