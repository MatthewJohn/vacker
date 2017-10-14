
from bson.objectid import ObjectId
import datetime

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

    def compare_file(self, file):
        analyser = vacker.analyser.Analyser()
        media_object = self.get_media_by_path(file)
        return (analyser.get_checksum(file) == media_object.get_checksum())

    def get_years(self):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$group': {'_id': '$y'}}])
        years = [item['_id'] for item in res if item['_id'] is not None]
        years.sort()
        return years

    def get_months(self, year):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': {'y': year}}, {'$group': {'_id': '$m'}}])
        months = [item['_id'] for item in res if item['_id'] is not None]
        months.sort()
        return months

    def get_days(self, year, month):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': {'y': year, 'm': month}}, {'$group': {'_id': '$d'}}])
        days = [item['_id'] for item in res if item['_id'] is not None]
        days.sort()
        return days

    def get_events_by_date(self, start_date, length=datetime.timedelta(hours=24)):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': {'datetime': {'$gte': start_date,
                                                                      '$lt': (start_date + length)}}},
                                             {'$group': {'_id': '$event_id'}}])
        event_details = []
        for event_id in [item['_id'] for item in res]:
            
            event_details.append({'id': str(event_id),
                                  'name': None,
                                  'media_count': len(self.get_sets_by_event(str(event_id)))})
        return event_details


    def get_sets_by_event(self, event_id):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': {'event_id': ObjectId(event_id)}},
                                             {'$group': {'_id': '$set_id'}}])
        return [str(set_obj['_id']) for set_obj in res]

    def get_sets_by_date(self, start_date, length=datetime.timedelta(hours=24)):
        pass

    def get_media_by_set(self, set_id):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.find({'set_id': ObjectId(set_id)})
        return [str(media['_id']) for media in res]

    def get_media_by_event(self, event_id):
        pass

    def get_media_by_date(self, start_date, length=datetime.timedelta(hours=24)):
        pass

    def get_random_media_by_date(self, start_date, end_date):
        db_connection = vacker.database.Database.get_database()
        media = db_connection.media.aggregate([
            {'$match': {'datetime': {'$gte': start_date, '$lt': end_date}}},
            {'$sample': {'size': 1}}
        ])
        for media_itx in media:
            return self.get_media_by_id(str(media_itx['_id']))
        return None

    def get_random_media_by_event(self, event_id):
        db_connection = vacker.database.Database.get_database()
        media = db_connection.media.aggregate([
            {'$match': {'event_id': ObjectId(event_id)}},
            {'$sample': {'size': 1}}
        ])
        for media_itx in media:
            return self.get_media_by_id(str(media_itx['_id']))
        return None

    def get_random_media_by_set(self, set_id):
        db_connection = vacker.database.Database.get_database()
        media = db_connection.media.aggregate([
            {'$match': {'set_id': ObjectId(set_id)}},
            {'$sample': {'size': 1}}
        ])
        for media_itx in media:
            return self.get_media_by_id(str(media_itx['_id']))
        return None