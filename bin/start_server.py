#!/usr/bin/python

import sys
sys.path.append('.')

from vacker.server import app

app.run(debug=True, threaded=True)
