
from bson.objectid import ObjectId
import datetime

import vacker.database
import vacker.config


class File(object):

    def __init__(self, file_id, document=None):
        self._id = file_id
        self._document = self._get_document() if document is None else document

    def _get_document(self):
        pass

    def get_id(self):
        return self._id

    def get_path(self):
        return self._document['g_path']

    def get_mime_type(self):
        return self._document['g_mime_type']

    def get_checksums(self):
        return self._document['g_sha1'], self._document['g_sha512']

    def delete(self):
        database_connection = vacker.database.Database.get_database()
        database_connection.media.remove({'_id': ObjectId(self.get_id())})

    def _get_thumbnail_path(self):
        return '{0}/{1}'.format(
            vacker.config.Config.get('THUMBNAIL_DIR'),
            self._document['g_sha512'])

    def get(self, attr, default_val=None):
        return self._document.get(attr, default_val)

    def get_thumbnail(self):
        return self._get_thumbnail_path()

