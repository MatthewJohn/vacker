
from bson.objectid import ObjectId
import datetime

import vacker.media_collection
import vacker.database
import vacker.media.photo
import vacker.media.video
import vacker.analyser

class MediaFactory(object):

    def get_media_by_path(self, path):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.find({'path': path})
        if not res.count():
            return None
        return self.get_media_by_id(str(res[0]['_id']))

    def get_media_date_range(self, datetime_obj, time_difference):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.find({'datetime': {'$gt': (datetime_obj - time_difference),
                                                     '$lt': (datetime_obj + time_difference)}})
        return [item for item in res]

    def get_media_by_id(self, media_id):
        return vacker.media.photo.Photo(ObjectId(media_id))

    def get_media_by_checksum(self, checksum):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.find({'checksum': checksum})
        if not res.count():
            return None
        return self.get_media_by_id(str(res[0]['_id']))

    def compare_file(self, file):
        analyser = vacker.analyser.Analyser()
        media_object = self.get_media_by_path(file)
        return (analyser.get_checksum(file) == media_object.get_checksum())
