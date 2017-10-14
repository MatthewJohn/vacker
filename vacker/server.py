
from flask import Flask, Response, abort
from flask_restful import Resource, Api
import datetime

import vacker.media_factory


app = Flask(__name__)
api = Api(app)

@app.route('/thumbnail/<string:media_id>')
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
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_years()

class GetMonths(Resource):
    def get(self, year):
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_months(year)

class GetDays(Resource):
    def get(self, year, month):
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_days(year, month)

class GetEvents(Resource):
    def get(self, year, month, day):
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_events_by_date(datetime.datetime(year=year, month=month, day=day))

class GetSets(Resource):
    def get(self, event_id):
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_sets_by_event(event_id)

class GetMedia(Resource):
    def get(self, set_id):
        media_factory = vacker.media_factory.MediaFactory()
        return media_factory.get_media_by_set(set_id)

api.add_resource(GetYears, '/years')
api.add_resource(GetMonths, '/years/<int:year>/months')
api.add_resource(GetDays, '/years/<int:year>/months/<int:month>/days')
api.add_resource(GetEvents, '/years/<int:year>/months/<int:month>/days/<int:day>/events')
api.add_resource(GetSets, '/events/<string:event_id>/sets')
api.add_resource(GetMedia, '/sets/<string:set_id>/media')
