
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

@app.route('/date/<int:date_id>/thumbnail')
def get_date_thumbnail(date_id):
    collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
    if show_hidden():
        collection.show_hidden()
    media_id = collection.get_random_thumbnail()
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

class GetDateDetails(Resource):
    def get(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.get_details()

class ToggleDateBackup(Resource):
    def post(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.toggle_backup()

class ToggleDateHide(Resource):
    def post(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.toggle_hide()

class GetMonths(Resource):
    def get(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.get_child_months()

class GetDays(Resource):
    def get(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.get_child_days()

class GetSets(Resource):
    def get(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.get_child_sets()

class GetMediaByDate(Resource):
    def get(self, date_id):
        collection = vacker.media_collection.DateCollection.getCollectionFromDateId(date_id)
        if show_hidden():
            collection.show_hidden()
        return collection.get_media_ids()

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
api.add_resource(GetDateDetails, '/date/<int:date_id>')
api.add_resource(ToggleDateBackup, '/date/<int:date_id>/backup')
api.add_resource(ToggleDateHide, '/date/<int:year>/hide')
api.add_resource(GetMonths, '/date/<int:date_id>/months')
api.add_resource(GetDays, '/date/<int:date_id>/days')
api.add_resource(GetSets, '/date/<int:date_id>/sets')
api.add_resource(GetMediaByDate, '/date/<int:date_id>/media')

# Set APIs
api.add_resource(GetSetDetails, '/sets/<string:set_id>')
api.add_resource(ToggleSetBackup, '/sets/<string:set_id>/backup')
api.add_resource(ToggleSetHide, '/sets/<string:set_id>/hide')
api.add_resource(GetMediaBySet, '/sets/<string:set_id>/media')

# Photo
api.add_resource(GetPhoto, '/media/<string:media_id>')
api.add_resource(ToggleMediaBackup, '/media/<string:media_id>/backup')
api.add_resource(ToggleMediaHide, '/media/<string:media_id>/hide')
