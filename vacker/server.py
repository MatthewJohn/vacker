
from flask import Flask, Response, abort, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import datetime

import vacker.media_factory
import vacker.media_collection


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

def show_hidden():
    if 'show_hidden' in request.args and str(request.args['show_hidden']) == '1':
        return True
    try:
        if 'show_hidden' in request.get_json() and request.get_json()['show_hidden'] == True:
            return True
    except:
        pass
    return False

@app.route('/media/<string:media_id>/data')
def get_media_data(media_id):
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
    year_collection = vacker.media_collection.YearCollection(year=year)
    if show_hidden():
        year_collection.show_hidden()
    media_id = year_collection.get_random_thumbnail()
    if not media_id:
        abort(404)
    return get_thumbnail(media_id)

@app.route('/years/<int:year>/months/<int:month>/thumbnail')
def get_month_thumbnail(year, month):
    month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
    if show_hidden():
        month_collection.show_hidden()
    media_id = month_collection.get_random_thumbnail()
    if not media_id:
        abort(404)
    return get_thumbnail(media_id)

@app.route('/years/<int:year>/months/<int:month>/days/<int:day>/thumbnail')
def get_day_thumbnail(year, month, day):
    day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
    if show_hidden():
        day_collection.show_hidden()
    media_id = day_collection.get_random_thumbnail()
    if not media_id:
        abort(404)
    return get_thumbnail(media_id)

@app.route('/sets/<string:set_id>/thumbnail')
def get_set_thumbnail(set_id):
    set_collection = vacker.media_collection.SetCollection(id=set_id)
    if show_hidden():
        set_collection.show_hidden()
    media_id = set_collection.get_random_thumbnail()
    if not media_id:
        abort(404)
    return get_thumbnail(media_id)

class GetYears(Resource):
    def get(self):
        all_collection = vacker.media_collection.AllMedia()
        if show_hidden():
            all_collection.show_hidden()
        return all_collection.get_years()

class GetYearDetails(Resource):
    def get(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        if show_hidden():
            year_collection.show_hidden()
        return year_collection.get_details()

class ToggleYearBackup(Resource):
    def post(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        if show_hidden():
            year_collection.show_hidden()
        return year_collection.toggle_backup()

class ToggleYearHide(Resource):
    def post(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        if show_hidden():
            year_collection.show_hidden()
        return year_collection.toggle_hide()

class GetMonths(Resource):
    def get(self, year):
        year_collection = vacker.media_collection.YearCollection(year=year)
        if show_hidden():
            year_collection.show_hidden()
        return year_collection.get_child_months()

class GetMonthDetails(Resource):
    def get(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        if show_hidden():
            month_collection.show_hidden()
        return month_collection.get_details()

class ToggleMonthBackup(Resource):
    def post(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        if show_hidden():
            month_collection.show_hidden()
        return month_collection.toggle_backup()

class ToggleMonthHide(Resource):
    def post(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        if show_hidden():
            month_collection.show_hidden()
        return month_collection.toggle_hide()

class GetDays(Resource):
    def get(self, year, month):
        month_collection = vacker.media_collection.MonthCollection(year=year, month=month)
        if show_hidden():
            month_collection.show_hidden()
        return month_collection.get_child_days()

class GetDayDetails(Resource):
    def get(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        if show_hidden():
            day_collection.show_hidden()
        return day_collection.get_details()

class ToggleDayBackup(Resource):
    def post(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        if show_hidden():
            day_collection.show_hidden()
        return day_collection.toggle_backup()

class ToggleDayHide(Resource):
    def post(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        if show_hidden():
            print 'hiddden'
            day_collection.show_hidden()
        return day_collection.toggle_hide()

class GetSetsByDay(Resource):
    def get(self, year, month, day):
        day_collection = vacker.media_collection.DayCollection(year=year, month=month, day=day)
        if show_hidden():
            day_collection.show_hidden()
        return day_collection.get_child_sets()

class GetSetDetails(Resource):
    def get(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        if show_hidden():
            set_collection.show_hidden()
        return set_collection.get_details()

class ToggleSetBackup(Resource):
    def post(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        if show_hidden():
            set_collection.show_hidden()
        return set_collection.toggle_backup()

class ToggleSetHide(Resource):
    def post(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        if show_hidden():
            set_collection.show_hidden()
        return set_collection.toggle_hide()

class GetMediaBySet(Resource):
    def get(self, set_id):
        set_collection = vacker.media_collection.SetCollection(id=set_id)
        if show_hidden():
            set_collection.show_hidden()
        return set_collection.get_media_ids()

class GetPhoto(Resource):
    def get(self, media_id):
        media_factory = vacker.media_factory.MediaFactory()
        media = media_factory.get_media_by_id(media_id)
        return media.get_details()

class ToggleMediaBackup(Resource):
    def post(self, media_id):
        media_factory = vacker.media_factory.MediaFactory()
        media = media_factory.get_media_by_id(media_id)
        return media.toggle_backup()

class ToggleMediaHide(Resource):
    def post(self, media_id):
        media_factory = vacker.media_factory.MediaFactory()
        media = media_factory.get_media_by_id(media_id)
        return media.toggle_hide()


# Year API
api.add_resource(GetYears, '/years')
api.add_resource(GetYearDetails, '/years/<int:year>')
api.add_resource(ToggleYearBackup, '/years/<int:year>/backup')
api.add_resource(ToggleYearHide, '/years/<int:year>/hide')
api.add_resource(GetMonths, '/years/<int:year>/months')

# Month APIs
api.add_resource(GetMonthDetails, '/years/<int:year>/months/<int:month>')
api.add_resource(ToggleMonthBackup, '/years/<int:year>/months/<int:month>/backup')
api.add_resource(ToggleMonthHide, '/years/<int:year>/months/<int:month>/hide')
api.add_resource(GetDays, '/years/<int:year>/months/<int:month>/days')

# Day APIs
api.add_resource(GetDayDetails, '/years/<int:year>/months/<int:month>/days/<int:day>')
api.add_resource(ToggleDayBackup, '/years/<int:year>/months/<int:month>/days/<int:day>/backup')
api.add_resource(ToggleDayHide, '/years/<int:year>/months/<int:month>/days/<int:day>/hide')
api.add_resource(GetSetsByDay, '/years/<int:year>/months/<int:month>/days/<int:day>/sets')

# Set APIs
api.add_resource(GetSetDetails, '/sets/<string:set_id>')
api.add_resource(ToggleSetBackup, '/sets/<string:set_id>/backup')
api.add_resource(ToggleSetHide, '/sets/<string:set_id>/hide')
api.add_resource(GetMediaBySet, '/sets/<string:set_id>/media')

# Photo
api.add_resource(GetPhoto, '/media/<string:media_id>')
api.add_resource(ToggleMediaBackup, '/media/<string:media_id>/backup')
api.add_resource(ToggleMediaHide, '/media/<string:media_id>/hide')
