
from flask import Flask, Response, abort
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import datetime

import vacker.media_factory
import vacker.media_collection


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/photo/<string:media_id>/data')
def get_photo_data(media_id):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_media_by_id(media_id)
    response = Response(media.get_photo_data(), mimetype=media.get_mime_type())
    return response

@app.route('/media/<string:media_id>/thumbnail')
def get_thumbnail(media_id):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_media_by_id(media_id)
    response = Response(media.get_thumbnail(), mimetype='image/jpeg')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/years/<int:year>/thumbnail')
def get_year_thumbnail(year):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_random_media_by_date(
        datetime.datetime(year=year, month=1, day=1),
        datetime.datetime(year=(year + 1), month=1, day=1)
    )
    if not media:
        abort(404)
    return get_thumbnail(media.get_id())

@app.route('/years/<int:year>/months/<int:month>/thumbnail')
def get_month_thumbnail(year, month):
    media_factory = vacker.media_factory.MediaFactory()
    end_date = datetime.datetime(year=(year + 1), month=1, day=1) if month == 12 else datetime.datetime(year=year, month=(month + 1), day=1)
    media = media_factory.get_random_media_by_date(
        datetime.datetime(year=year, month=month, day=1),
        end_date
    )
    if not media:
        abort(404)
    return get_thumbnail(media.get_id())

@app.route('/years/<int:year>/months/<int:month>/days/<int:day>/thumbnail')
def get_day_thumbnail(year, month, day):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_random_media_by_date(
        datetime.datetime(year=year, month=month, day=day),
        (datetime.datetime(year=year, month=month, day=day) + datetime.timedelta(hours=24))
    )
    if not media:
        abort(404)
    return get_thumbnail(media.get_id())

@app.route('/events/<string:event_id>/thumbnail')
def get_event_thumbnail(event_id):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_random_media_by_event(event_id)
    if not media:
        abort(404)
    return get_thumbnail(media.get_id())

@app.route('/sets/<string:set_id>/thumbnail')
def get_set_thumbnail(set_id):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_random_media_by_set(set_id)
    if not media:
        abort(404)
    return get_thumbnail(media.get_id())

class GetYears(Resource):
    def get(self):
        all_collection = vacker.media_collection.AllMedia()
        return all_collection.get_years()

class GetYearDetails(Resource):
    def get(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        return year_collection.get_details()

class ToggleYearBackup(Resource):
    def post(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        return year_collection.toggle_backup()

class GetMonths(Resource):
    def get(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        return year_collection.get_child_months()

class GetMonthDetails(Resource):
    def get(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        return month_collection.get_details()

class ToggleMonthBackup(Resource):
    def post(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        return month_collection.toggle_backup()


class GetDays(Resource):
    def get(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        return month_collection.get_child_days()

class GetDayDetails(Resource):
    def get(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        return day_collection.get_details()

class ToggleDayBackup(Resource):
    def post(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        return day_collection.toggle_backup()

class GetSetsByDay(Resource):
    def get(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        return day_collection.get_child_sets()

class GetSetDetails(Resource):
    def get(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        return set_collection.get_details()

class ToggleSetBackup(Resource):
    def post(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        return set_collection.toggle_backup()

class GetMediaBySet(Resource):
    def get(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        return set_collection.get_media_ids()

class GetPhoto(Resource):
    def get(self, media_id):
        media_factory = vacker.media_factory.MediaFactory()
        media = media_factory.get_media_by_id(media_id)
        return {'orientation': media.get_orientation()}

class ToggleMediaBackup(Resource):
    def post(self, media_id):
        media_factory = vacker.media_factory.MediaFactory()
        media = media_factory.get_media_by_id(media_id)
        return media.toggle_backup()



# Year API
api.add_resource(GetYears, '/years')
api.add_resource(GetYearDetails, '/years/<int:year>')
api.add_resource(ToggleYearBackup, '/years/<int:year>/backup')
api.add_resource(GetMonths, '/years/<int:year>/months')

# Month APIs
api.add_resource(GetMonthDetails, '/years/<int:year>/months/<int:month>')
api.add_resource(ToggleMonthBackup, '/years/<int:year>/months/<int:month>/backup')
api.add_resource(GetDays, '/years/<int:year>/months/<int:month>/days')

# Day APIs
api.add_resource(GetDayDetails, '/years/<int:year>/months/<int:month>/days/<int:day>')
api.add_resource(ToggleDayBackup, '/years/<int:year>/months/<int:month>/days/<int:day>/backup')
api.add_resource(GetSetsByDay, '/years/<int:year>/months/<int:month>/days/<int:day>/sets')

# Set APIs
api.add_resource(GetSetDetails, '/sets/<string:set_id>')
api.add_resource(ToggleSetBackup, '/sets/<string:set_id>/backup')
api.add_resource(GetMediaBySet, '/sets/<string:set_id>/media')

# Photo
api.add_resource(GetPhoto, '/photo/<string:media_id>')
api.add_resource(ToggleMediaBackup, '/photo/<string:media_id>/backup')
