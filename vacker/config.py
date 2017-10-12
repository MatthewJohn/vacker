

class Config(object):

    DEFAULT_CONFIG = {
        'MONGO_HOST': 'localhost',
        'MONGO_PORT': 27017,
        'MONGO_DATABASE': 'vacker',
        'DEFAULT_SET_INTERVAL': 15,
        'DEFAULT_EVENT_INTERVAL': 7200
    }

    @staticmethod
    def get(key):
        if key in Config.DEFAULT_CONFIG:
            return Config.DEFAULT_CONFIG[key]
