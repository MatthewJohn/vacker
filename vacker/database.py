
#from pymongo import MongoClient
import pysolr

from vacker.config import Config


class Database(object):
    CONNECTION = None

    MAX_BATCH_SIZE = 100

    def __init__(self):
        self._batch = []
        Database._solr_conn = pysolr.Solr(Config.get('SOLR_URL'))

    @staticmethod
    def get_database():
        return Database._solr_conn
        if Database.CONNECTION is None:
            Database.CONNECTION = MongoClient(Config.get('MONGO_HOST'), Config.get('MONGO_PORT'))
        return Database.CONNECTION[Config.get('MONGO_DATABASE')]

    def insert_batch(self, _document):
        self._batch.append(_document)
        if len(self._batch) >= self.MAX_BATCH_SIZE:
            self.complete_batch()

    def complete_batch(self):
        self._solr_conn.add(self._batch, commit=True)
        self._batch = []
