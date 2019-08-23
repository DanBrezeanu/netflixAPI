from settings import HEADER_KEY, HEADER_HOST, API_URL, CACHE_FILE
from models.CacheManager import CacheManager
import requests
import json
from sys import stderr
import os

def api_call(query_params):
    cache = CacheManager.getInstance()
    headers = dict((HEADER_HOST, HEADER_KEY))

    cache_response = cache.loadFromCache(query_params)
    if cache_response is not None:
        return cache_response

    response = requests.request("GET", API_URL, headers = headers, params = query_params)

    if response.status_code == 200:
        CacheManager.getInstance().saveToCache(query_params, JSONite(response))

    return JSONite(response) if response.status_code == 200 else None

def JSONite(response):
    if response is None:
        return None

    return json.loads(response.text)

def log_error(message):
    print(message, file=stderr)

def request_log(function, progress, total):
    print("[REQUEST] [{}] {}/{} received".format(function.f_code.co_name, progress, total))

def clear_cache():
    os.remove(CACHE_FILE)
