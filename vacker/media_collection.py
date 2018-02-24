
from bson.objectid import ObjectId

import vacker.database


class MediaCollection(object):

    def __init__(self, id):
        self._show_hidden = False
        self._id = id
        self._initialise()

    def _initialise(self):
        pass

    def show_hidden(self):
        self._show_hidden = True

    def get_media_ids(self):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': self._get_media_filter()}])
        child_ids = [str(item['_id']) for item in res if item['_id'] is not None]
        child_ids.sort()
        return child_ids

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_details(self):
        return {
            'id': self.get_id(),
            'name': self.get_name(),
            'media_count': self.get_media_count(),
            'backup_state': self.get_backup_state(),
            'hidden_state': self.get_hidden_state()
        }

    def get_backup_state(self):
        """
        Determines the backup state of the media in the collection.
        Returns 0 - No media is backed up
                1 - Some media is backed up
                2 - All media is backed up
        """
        media_filter = self._get_media_filter()
        media_filter['backup'] = True
        db_connection = vacker.database.Database.get_database()
        backup_count = db_connection.media.find(media_filter).count()
        if backup_count == 0:
            return 0
        if backup_count < self.get_media_count():
            return 1
        return 2


    def toggle_backup(self):
        current_backup_state = self.get_backup_state()
        if current_backup_state == 1:
            return False
        new_backup_state = False if (current_backup_state == 2) else True
        db_connection = vacker.database.Database.get_database()
        db_connection.media.update(self._get_media_filter(), {'$set': {'backup': new_backup_state}}, multi=True)
        return True

    def get_hidden_state(self):
        """
        Determines the hidden state of the media in the collection.
        Returns 0 - No media is hidden
                1 - Some media is hidden
                2 - All media is hidden
        """
        media_filter = self._get_media_filter()
        media_filter['hide'] = True
        db_connection = vacker.database.Database.get_database()
        hidden_count = db_connection.media.find(media_filter).count()
        # If none are hidden, return 0
        if hidden_count == 0:
            return 0

        # If all are hiden, return 2
        if hidden_count == self.get_media_count():
            return 2
        # If hidden has not been specified, return 0, as none shown
        # will be hidden
        if not self._show_hidden:
            return 0
        # Otherwise, if some are hidden (but hidden are shown), use this status
        if hidden_count < self.get_media_count():
            return 1

    def toggle_hide(self):
        current_hidden_state = self.get_hidden_state()
        new_hidden_state = False if (current_hidden_state == 2) else True
        db_connection = vacker.database.Database.get_database()
        db_connection.media.update(self._get_media_filter(), {'$set': {'hide': new_hidden_state}}, multi=True)
        return True

    def _get_media_filter(self):
        if self._show_hidden:
            return {}
        else:
            return {'hide': False}

    def get_media_count(self):
        db_connection = vacker.database.Database.get_database()
        return db_connection.media.find(self._get_media_filter()).count()

    def _get_child_ids(self, child_type):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.media.aggregate([{'$match': self._get_media_filter()}, {'$group': {'_id': child_type}}])
        child_ids = [str(item['_id']) for item in res if item['_id'] is not None]
        child_ids.sort()
        return child_ids

    def get_child_sets(self):
        return self._get_child_ids('$set_id')


class DateCollection(MediaCollection):

    def get_year(self):
        return self._year

    def get_month(self):
        return self._month

    def get_day(self):
        return self._day

    def get_child_months(self):
        return self._get_child_ids('$m')

    def get_child_days(self):
        return self._get_child_ids('$d')

    def get_child_events(self):
        return self._get_child_ids('$event_id')

class AllMedia(DateCollection):

    def __init__(self):
        self._show_hidden = False

    def get_years(self):
        return self._get_child_ids('$y')


class YearCollection(DateCollection):
    
    def __init__(self, year):
        super(YearCollection, self).__init__(year)
        self._year = year

    def _get_media_filter(self):
        media_filter = super(YearCollection, self)._get_media_filter()
        media_filter['y'] = self.get_year()
        return media_filter

    def get_name(self):
        return self.get_id()


class MonthCollection(DateCollection):
    
    def __init__(self, year, month):
        super(MonthCollection, self).__init__(month)
        self._year = year
        self._month = month

    def get_name(self):
        return ['Jan', 'Feb', 'March', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'][int(self.get_id()) - 1]

    def _get_media_filter(self):
        media_filter = super(MonthCollection, self)._get_media_filter()
        media_filter['y'] = self.get_year()
        media_filter['m'] = self.get_month()
        return media_filter


class DayCollection(DateCollection):
    
    def __init__(self, year, month, day):
        super(DayCollection, self).__init__(day)
        self._year = year
        self._month = month
        self._day = day

    def get_name(self):
        str_id = str(self.get_id())
        if str_id.endswith('1'):
            return '%s%s' % (str_id, 'st')
        if str_id.endswith('2'):
            return '%s%s' % (str_id, 'nd')
        if str_id.endswith('3'):
            return '%s%s' % (str_id, 'rd')
        return '%s%s' % (str_id, 'th')

    def _get_media_filter(self):
        media_filter = super(DayCollection, self)._get_media_filter()
        media_filter['y'] = self.get_year()
        media_filter['m'] = self.get_month()
        media_filter['d'] = self.get_day()
        return media_filter


class SetCollection(MediaCollection):

    def _get_media_filter(self):
        media_filter = super(SetCollection, self)._get_media_filter()
        media_filter['set_id'] = ObjectId(self.get_id())
        return media_filter

    def _initialise(self):
        db_connection = vacker.database.Database.get_database()
        res = db_connection.sets.find({'_id': ObjectId(self.get_id())})
        if not res.count():
            raise Exception('Set does not exist: ' % self.get_id())

        self._name = res[0]['name'] or ''
