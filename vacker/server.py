
from flask import Flask, Response, abort, request
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
            query_string=request.args.get('search[value]', ''),
            start=request.args.get('start', 0),
            limit=request.args.get('length', 10))
        return {
            'data': [file_ for file_ in res['files']],
            'recordsTotal': res['total_results'],
            'recordsFiltered': res['total_results']
        }


# Year API
api.add_resource(Stats, '/stats/<string:query_string>')
api.add_resource(Search, '/search')
