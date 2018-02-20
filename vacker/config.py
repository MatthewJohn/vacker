

class Config(object):

    DEFAULT_CONFIG = {
        'MONGO_HOST': 'localhost',
        'MONGO_PORT': 27017,
        'MONGO_DATABASE': 'vacker',
        'DEFAULT_SET_INTERVAL': 30,
        'DEFAULT_EVENT_INTERVAL': 1800,
        # Allow for any variation of 500x500, e.g. 250x1000
        'MINIMUM_RESOLUTION': 250000
    }

    @staticmethod
    def get(key):
        if key in Config.DEFAULT_CONFIG:
            return Config.DEFAULT_CONFIG[key]

