
from pymongo import MongoClient

from vacker.config import Config

class Database(object):
    CONNECTION = None

    @staticmethod
    def get_database():
        if Database.CONNECTION is None:
            Database.CONNECTION = MongoClient(Config.get('MONGO_HOST'), Config.get('MONGO_PORT'))
        return Database.CONNECTION[Config.get('MONGO_DATABASE')]
