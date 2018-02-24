
from bson.objectid import ObjectId
import datetime

import vacker.media_factory
import vacker.database
import vacker.config


class Media(object):
    
    def __init__(self, media_id):
        self._id = media_id

    def get_id(self):
        return self._id

    def get_date(self):
        database_connection = vacker.database.Database.get_database()
        return database_connection.media.find_one({'_id': ObjectId(self.get_id())})['datetime']

    def get_path(self):
        database_connection = vacker.database.Database.get_database()
        return database_connection.media.find_one({'_id': ObjectId(self.get_id())})['path']

    def get_orientation(self):
        database_connection = vacker.database.Database.get_database()
        return database_connection.media.find_one({'_id': ObjectId(self.get_id())})['orientation'] 

    def get_mime_type(self):
        database_connection = vacker.database.Database.get_database()
        return database_connection.media.find_one({'_id': ObjectId(self.get_id())})['mime_type'] 

    def update_sets(self):
        if not self.get_date():
            return
        database_connection = vacker.database.Database.get_database()
        media_factory = vacker.media_factory.MediaFactory()
        surround_media = media_factory.get_media_date_range(
            self.get_date(), datetime.timedelta(seconds=vacker.config.Config.get('DEFAULT_SET_INTERVAL'))
        )
        surround_media.sort(key=lambda x: x['datetime'])
        sets = [x['set_id'] for x in surround_media if x['set_id'] is not None]

        # Create set/get set ID and update all media
        set_id = sets[0] if len(sets) else database_connection.sets.insert_one({'auto': True, 'backup_state': False, 'name': '', 'hidden': False}).inserted_id
        database_connection.media.update({'_id': {'$in': [x['_id'] for x in surround_media]}},
                                         {'$set': {'set_id': set_id}}, multi=True)
        database_connection.media.update({'set_id': {'$in': sets}},
                                         {'$set': {'set_id': set_id}}, multi=True)

    def update_events(self):
        if not self.get_date():
            return
        database_connection = vacker.database.Database.get_database()
        media_factory = vacker.media_factory.MediaFactory()
        surround_media = media_factory.get_media_date_range(
            self.get_date(), datetime.timedelta(seconds=vacker.config.Config.get('DEFAULT_EVENT_INTERVAL'))
        )
        surround_media.sort(key=lambda x: x['datetime'])
        events = [x['event_id'] for x in surround_media if x['event_id'] is not None]

        # Create set/get set ID and update all media
        event_id = events[0] if len(events) else database_connection.events.insert_one({'auto': True, 'backup_state': False, 'name': '', 'hidden': False}).inserted_id
        database_connection.media.update({'_id': {'$in': [x['_id'] for x in surround_media]}},
                                         {'$set': {'event_id': event_id}}, multi=True)
        database_connection.media.update({'set_id': {'$in': events}},
                                         {'$set': {'event_id': event_id}}, multi=True)

    def get_thumbnail(self):
        database_connection = vacker.database.Database.get_database()
        return database_connection.thumbnail.find({'_id': self.get_id()})[0]['thumbnail_data']


