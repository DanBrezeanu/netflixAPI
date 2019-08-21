import os

API_KEY_FILE = 'api.key'

API_URL = 'https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi'
HEADER_HOST = ('x-rapidapi-host', 'unogs-unogs-v1.p.rapidapi.com')
HEADER_KEY  = ('x-rapidapi-key', open(API_KEY_FILE, 'r').read().strip())

COUNTRY_CODE = 'RO'

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
