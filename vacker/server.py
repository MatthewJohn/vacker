import urllib
from flask import Flask, Response, abort, request, send_file
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import datetime
import json

import vacker.file_factory



app = Flask(__name__)
api = Api(app)
file_factory = vacker.file_factory.FileFactory()

CORS(app, resources={"*": {"origins": "*"}})


class Stats(Resource):

    def get(self, query_string):
        pass


class Search(Resource):

    def get(self):
        res = file_factory.query_files(
            query_string=request.args.get('q', ''),
            start=request.args.get('start', 0),
            limit=request.args.get('length', 10),
            sort=request.args.get('order_col', None),
            sort_dir=request.args.get('order_dir', None))
        for file_ in res['files']:
            file_['g_file_name'] = '<a href="/blob/{0}" target="_blankn">{1}</a>'.format(urllib.parse.quote(file_['id']), file_['g_file_name'])
        return {
            'data': [file_ for file_ in res['files']],
            'recordsTotal': res['total_results'],
            'recordsFiltered': res['total_results']
        }

class Blob(Resource):

    def get(self, file_id):
        file_ = file_factory.get_file_by_id(file_id)
        parent = file_.get('a_parent_archive')
        if parent:
            return send_file(parent)
        return send_file(file_.get_path())


# Year API
api.add_resource(Stats, '/stats/<string:query_string>')
api.add_resource(Search, '/search')
api.add_resource(Blob, '/blob/<string:file_id>')
