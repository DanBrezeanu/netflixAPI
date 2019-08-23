from settings import COUNTRY_CODE, RESPONSES_PER_PAGE, VERBOSE
from base import api_call, request_log
from models.NetflixTitle import NetflixTitle
from models.NetflixDatabase import NetflixDatabase
import os, sys

def new_releases(days_to_query = 7):
    page = 1
    finished_pages = False
    netflix_titles = []
    items_received = 0

    while not finished_pages:
        options = {'q': 'get:new' + str(days_to_query) + ':'+ COUNTRY_CODE, 'p': str(page), 't': 'ns', 'st': 'adv'}

        response = api_call(options)
        if response is None:
            return [None]

        items_received += len(response['ITEMS'])

        if VERBOSE:
            request_log(sys._getframe(), items_received, response['COUNT'])

        for title in response['ITEMS']:
            netflix_titles.append(NetflixTitle(title))

        if items_received >= int(response['COUNT']):
            finished_pages = True
        else:
            page += 1

    return netflix_titles

def countries_list():
    options = {'t': 'lc', 'q': 'available'}
    items_received = 0

    response = api_call(options)
    if response is None:
        return [None]

    items_received += len(response['ITEMS'])

    if VERBOSE:
        request_log(sys._getframe(), items_received, response['COUNT'])

    netflix_countries = []
    for country in response['ITEMS']:
        netflix_countries.append(tuple(country[:3]))

    return netflix_countries

def genres_list():
    options = {'t': 'genres'}
    items_received = 0

    response = api_call(options)
    if response is None:
        return [None]

    items_received += len(response['ITEMS'])

    if VERBOSE:
        request_log(sys._getframe(), items_received, response['COUNT'])


    netflix_genres = {}
    for genre in response['ITEMS']:
        netflix_genres = {**netflix_genres, **genre}

    return netflix_genres

def advanced_search(start_imdb_rating = '0', sort_by = 'Relevance', start_year = '1900', genre_id = '10673,10702,11804,11828,1192487,1365,1568,2125,2653,43040,43048,4344,46576,75418,76501,77232,788212,801362,852490,899,9584'):
    #10673,10702,11804,11828,1192487,1365,1568,2125,2653,43040,43048,4344,46576,75418,76501,77232,788212,801362,852490,899,9584
    items_received = 0
    finished_pages = False
    netflix_titles = []

    start_netflix_rating = '0'
    end_netflix_rating = '5'
    end_imdb_rating = '10'
    # start_imdb_rating = '0'
    subtitle = 'Any'
    # sort_by = 'Relevance' #  Relevance, Date, Rating, Title, VideoType, FilmYear, Runtime
    # start_year = '1900'
    end_year = '2019'
    video_type = 'Any' # Any, Movie, Series
    audio_type = 'Any' # English, Chinese
    # genre_id = '0' # 0 == any
    page = 1
    clist = '400' # country
    query = '' # get:new10000
    imdb_votes = 'gt0' # gt[num] or lt[num]
    and_or = 'and'

    while not finished_pages:
        options = {'q': query                                            + '-!' + \
                        start_year           + ',' + end_year            + '-!' + \
                        start_netflix_rating + ',' + end_netflix_rating  + '-!' + \
                        start_imdb_rating    + ',' + end_imdb_rating     + '-!' + \
                        genre_id                                         + '-!' + \
                        video_type                                       + '-!' + \
                        audio_type                                       + '-!' + \
                        subtitle                                         + '-!' + \
                        imdb_votes                                       + '-!' + \
                        '{downloadable}',
                    't': 'ns',
                    'cl': clist,
                    'st': 'adv',
                    'ob': sort_by,
                    'p': str(page),
                    'sa': and_or
                    }

        response = api_call(options)
        if response is None:
            return [None]

        items_received += len(response['ITEMS'])

        if VERBOSE:
            request_log(sys._getframe(), items_received, response['COUNT'])

        for title in response['ITEMS']:
            netflix_titles.append(NetflixTitle(title))

        if items_received >= int(response['COUNT']):
            finished_pages = True
        else:
            page += 1
    return netflix_titles

if __name__ == '__main__':
    with open('genres', 'w') as f:
        titles = new_releases(22)
        for t in titles:
            f.write(str(t) + '\n')
