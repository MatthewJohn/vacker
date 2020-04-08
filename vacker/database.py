
#from pymongo import MongoClient
import pysolr
import math

from vacker.config import Config


class Database(object):

    MAX_BATCH_SIZE = 500
    _CONNECTION = None
    _BATCH = []

    @staticmethod
    def get_database():
        if Database._CONNECTION is None:
            Database._CONNECTION = pysolr.Solr(Config.get('SOLR_URL'))
        return Database._CONNECTION

    def insert_batch(self, _document):
        print('Inserting..')
        Database._BATCH.append(_document)
        if len(Database._BATCH) >= self.MAX_BATCH_SIZE:
            self.complete_batch()

    def complete_batch(self):
        for n in range(math.ceil(len(Database._BATCH) / self.MAX_BATCH_SIZE)):
            self.get_database().add(Database._BATCH[n * self.MAX_BATCH_SIZE:(n + 1) * self.MAX_BATCH_SIZE], commit=True)
        Database._BATCH = []
