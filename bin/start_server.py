#!/usr/bin/python

import sys
sys.path.append('.')

from vacker.server import app
from vacker.config import Config

app.run(debug=bool(Config.get('DEBUG')), threaded=True, host=Config.get('LISTEN_HOST'))

