import settings
import requests
import json
from sys import stderr

def api_call(query_params):
    headers = dict((settings.HEADER_HOST, settings.HEADER_KEY))
    response = requests.request("GET", settings.API_URL, headers = headers, params = query_params)

    return response if response.status_code == 200 else None

def JSONite(response):
    if response is None:
        return None

    return json.loads(response.text)

def log_error(message):
    print(message, file=stderr)
