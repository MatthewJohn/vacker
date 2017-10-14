
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
    return Response(media.get_thumbnail(), mimetype='image/jpeg')

@app.route('/years/<int:year>/thumbnail')
def get_year_thumbnail(year):
    media_factory = vacker.media_factory.MediaFactory()
    media = media_factory.get_thumbnail_by_date(
        datetime.datetime(year=year, month=1, day=1), datetime.timedelta(days=365)
    )
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

api.add_resource(GetYears, '/years')
api.add_resource(GetMonths, '/years/<int:year>/months')
