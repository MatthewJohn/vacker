
import datetime

import vacker.media_collection
import vacker.database
import vacker.media.photo
import vacker.media.video
import vacker.media
import vacker.analyser


class FileFactory(object):

    def get_file_by_path(self, path):
        db_connection = vacker.database.Database.get_database()
        results = db_connection.search('g_path: "{0}"'.format(path))
        for res in results:
            return self.get_file_by_document(res)
        return None

    # def get_media_date_range(self, datetime_obj, time_difference):
    #     db_connection = vacker.database.Database.get_database()
    #     res = db_connection.media.find({'datetime': {'$gt': (datetime_obj - time_difference),
    #                                                  '$lt': (datetime_obj + time_difference)}})
    #     return [item for item in res]

    def get_file_by_id(self, file_id):

        return vacker.media.File(file_id)

    def get_file_by_document(self, document):
        return vacker.media.File(document['id'], document=document)

    def get_file_by_checksum(self, sha1, sha512):
        db_connection = vacker.database.Database.get_database()
        reuslts = db_connection.search('g_sha512: {sha512} AND g_sha1: {sha1}'.format(
            sha1=sha1, sha512=sha512))
        for res in reuslts:
            return self.get_file_by_document(res)
        return None

    def compare_file(self, file_path):
        analyser = vacker.analyser.Analyser()
        media_object = self.get_file_by_path(file_path)
        return analyser.get_checksums(file_path) == media_object.get_checksums()

    def query_files(self, query_values):
        outer_query_strings = []
        for query_value in query_values.split(' '):

            fields = ['g_file_name', 'g_size', 'g_path', 'g_extension', 'g_mime_type']
            query_string = ''
            query_fields = []
            for field in fields:
                query_fields.append(field + ': *{query_value}*')
            outer_query_strings.append('(' + ' OR '.join(query_fields).format(query_value=query_value) + ')')
        return vacker.database.Database.get_database().search(' AND '.join(outer_query_strings))

