"""
`appengine_config.py` is automatically loaded when Google App Engine
starts a new instance of your application. This runs before any
WSGI applications specified in app.yaml are loaded.
"""

import os
from google.appengine.ext import vendor

# Third-party libraries are stored in "lib"
_current_folder = os.path.dirname(os.path.abspath(__file__))
vendor.add(os.path.join(_current_folder, 'lib'))
