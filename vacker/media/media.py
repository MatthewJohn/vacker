
from bson.objectid import ObjectId
import datetime

import vacker.file_factory
import vacker.database
import vacker.config
from vacker.media import File


class Media(File):
    
    def get_date(self):
        return self._document.get('datetime', None)

    def get_orientation(self):
        return self._document.get('orientation', 0)

    def get_backup_state(self):
        return self._document['backup']

    def get_hidden_state(self):
        return self._document['hide']

    def update_sets(self):
        if not self.get_date():
            return
        database_connection = vacker.database.Database.get_database()
        file_factory = vacker.file_factory.FileFactory()
        surround_media = file_factory.get_media_date_range(
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
        file_factory = vacker.file_factory.FileFactory()
        surround_media = file_factory.get_media_date_range(
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

    def toggle_backup(self):
        database_connection = vacker.database.Database.get_database()
        current_backup_state = self.get_backup_state()
        database_connection.media.update({'_id': ObjectId(self.get_id())}, {'$set': {'backup': (not current_backup_state)}})
        return True

    def toggle_hide(self):
        database_connection = vacker.database.Database.get_database()
        current_hidden_state = self.get_hidden_state()
        database_connection.media.update({'_id': ObjectId(self.get_id())}, {'$set': {'hide': (not current_hidden_state)}})
        return True

    def get_details(self):
        return {
            'orientation': self.get_orientation(),
            'backup_state': 2 if self.get_backup_state() else 0,
            'hidden_state': 2 if self.get_hidden_state() else 0,
            'datetime': self.get_date().strftime('%a %d %b %H:%M:%S')
        }
