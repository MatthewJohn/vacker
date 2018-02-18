
import os
import datetime

import vacker.analyser
import vacker.media_factory
import vacker.database
import vacker.config


class Importer(object):

    def __init__(self):
        self.analyser = vacker.analyser.Analyser()
        self.media_factory = vacker.media_factory.MediaFactory()
        self.database = vacker.database.Database()

    def import_directory(self, directory, verify=False):
        for root, _, files in os.walk(directory):
            for file in files:
                self.import_file(os.path.join(root, file), verify=verify)

    def import_file(self, file, verify):
        file_type = self.analyser.detect_media_type(file)
        if file_type is vacker.analyser.MediaType.UNSUPPORTED:
            return False
        existing_file = self.media_factory.get_media_by_path(file)
        if existing_file and (not verify or self.media_factory.compare_file(file)):
            return False
        if file_type is vacker.analyser.MediaType.PHOTO:
            media_obj = self.import_photo(file)
            if not media_obj:
                return False
            media_obj.update_sets()
            media_obj.update_events()
            media_obj.create_thumbnail()
        elif file_type is vacker.analyser.MediaType.VIDEO:
            media_obj = self.import_video(file)
        return media_obj

    def import_photo(self, photo):
        analysed_info = self.analyser.get_image_data(photo)

        # Check is image is smaller than minimum resolution
        if (analysed_info['height'] * analysed_info['width']) < vacker.config.Config.get('MINIMUM_RESOLUTION'):
            return None

        analysed_info['checksum'] = self.analyser.get_checksum(photo)

        # Check if photo is a duplicate
        media_factory = vacker.media_factory.MediaFactory()
        dupe_media = media_factory.get_media_by_checksum(analysed_info['checksum'])
        if dupe_media:
            return None

        analysed_info['path'] = photo
        analysed_info['mtime'] = datetime.datetime.fromtimestamp(os.stat(photo).st_mtime)
        analysed_info['set_id'] = None
        analysed_info['event_id'] = None
        if 'datetime' in analysed_info and analysed_info['datetime']:
            analysed_info['y'] = analysed_info['datetime'].year
            analysed_info['m'] = analysed_info['datetime'].month
            analysed_info['d'] = analysed_info['datetime'].day

        photo_id = self.database.get_database().media.insert_one(analysed_info).inserted_id
        return vacker.media.photo.Photo(photo_id)

    def import_video(self, video):
        print 'you got vidz bro?'
