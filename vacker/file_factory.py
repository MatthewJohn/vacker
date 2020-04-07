
import datetime
import shlex
import sys

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
        db_connection = vacker.database.Database.get_database()
        results = db_connection.search('id: "{0}"'.format(file_id.replace('"', '')))
        for res in results:
            return self.get_file_by_document(res)
        return None

    def get_file_by_document(self, document):
        return vacker.media.File(document['id'], document=document)

    def get_file_by_checksum(self, shamean):
        db_connection = vacker.database.Database.get_database()
        reuslts = db_connection.search('g_shamean: {shamean}'.format(
            shamean=shamean))
        for res in reuslts:
            return self.get_file_by_document(res)
        return None

    def compare_file(self, file_path):
        analyser = vacker.analyser.Analyser()
        media_object = self.get_file_by_path(file_path)
        return analyser.get_checksums(file_path) == media_object.get_checksums()

    def query_files(self, query_string, start=0, limit=10, sort=None, sort_dir='desc'):
        outer_query_strings = []
        for query_value in shlex.split(query_string):

            fields = ['g_file_name', 'g_size', 'g_path', 'g_extension', 'g_mime_type', 'a_artist', 'm_title', 'a_album']
            #fields = ['*']
            query_fields = []
            for field in fields:
                if ' ' in query_value:
                    if field in ['g_file_name', 'g_path', 'a_artist', 'm_title', 'a_album']:
                        query_fields.append(field + ':"*{query_value}*"')
                else:
                    query_fields.append(field + ':*{query_value}*')
                #query_fields.append('*{query_value}*')
            outer_query_strings.append('(' + ' OR '.join(query_fields).format(query_value=query_value.replace('(', '\(').replace(')', '\)')) + ')')

        kwargs = {
            'start': start,
            'rows': limit
        }
        if sort:
            kwargs['sort'] = '{0} {1}'.format(sort, sort_dir)
        print('{!complexphrase}' + ' AND '.join(outer_query_strings), file=sys.stderr)
        res = vacker.database.Database.get_database().search(
            '{!complexphrase}' + ' AND '.join(outer_query_strings),
            **kwargs
            )
        return {
            'total_results': res.hits,
            'files': res.docs
        }

