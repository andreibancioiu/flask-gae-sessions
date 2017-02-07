import os
import secrets

is_development = os.environ.get('SERVER_SOFTWARE', 'Dev').startswith('Dev')

DEBUG = True
SECRET_KEY = "<development>"

if not is_development:
    DEBUG = False
    SECRET_KEY = mysecrets.SECRET_KEY
