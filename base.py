from settings import HEADER_KEY, HEADER_HOST, API_URL, CACHE_FILE
from typing import Callable
from models.CacheManager import CacheManager
import requests
import json
from sys import stderr
import os

def api_call(query_params: dict) -> dict:
    '''
    Makes a request to the API server if the given request is not cached.
    THIS SHOULD BE THE ONLY FUNCTION TO DIRECTLY ACCESS THE API SERVER, IN ORDER TO OPTIMIZE
    THE NUMBER OF CALLS MADE TO THE API

    :param query_params: dictionary containing the request parameters for the API call
    :type query_params: dict

    :returns: the response from the server
    :rtype: dict
    '''

    cache = CacheManager.getInstance()
    headers = dict((HEADER_HOST, HEADER_KEY))

    cache_response = cache.loadFromCache(query_params)
    if cache_response is not None:
        return cache_response

    response = requests.request("GET", API_URL, headers = headers, params = query_params)

    if response.status_code == 200:
        CacheManager.getInstance().saveToCache(query_params, JSONite(response))

    return JSONite(response) if response.status_code == 200 else None

def JSONite(response: requests.models.Response) -> dict:
    '''
    :param response: the response from the API server
    :type response: requests.models.Response

    :returns: json-ed response
    :rtype: dict
    '''
    if response is None:
        return None

    return json.loads(response.text)

def runtime_to_minutes(runtime: str) -> int:
    '''
    :param runtime: runtime of a given title
    :type runtime: str

    :returns: the number of minutes resulted from the given string
    :rtype: int
    '''
    if 'h' in runtime and 'm' in runtime:
        try:
            return int(runtime.split('h')[0]) * 60 + int(runtime.split('h')[-1].split('m')[0])
        except ValueError:
            log_error('[ERROR] Wrong format for runtime, must be "<nhours>h<nminutes>m"')
    elif 'm' in runtime:
        try:
            return int(runtime.split('m')[0])
        except ValueError:
            log_error('[ERROR] Wrong format for runtime, must be "<nhours>h<nminutes>m"')

def log_error(message: dict) -> None:
    '''
    Prints eror message to stderr

    :param message: the text to be printed
    :type message: str

    :returns: None
    '''
    print(message, file=stderr)

def request_log(function: Callable, progress: int, total: int) -> None:
    '''
    Pretty prints the progress for an API call

    :param function: the function which calls the API (through the api_call method)
    :type function: function

    :param progress: number of items received
    :type progress: int

    :param total: total number of items to be received
    :type total: int

    :returns: None
    '''
    print("[REQUEST] [{}] {}/{} received".format(function.f_code.co_name, progress, total))

def clear_cache() -> None:
    '''
    Removes the cache file

    :returns: None
    '''
    os.remove(CACHE_FILE)
