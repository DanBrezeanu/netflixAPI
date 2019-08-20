import settings
from base import JSONite, api_call
from models.NetflixTitle import NetflixTitle

def new_releases(days_to_query = 7):
    options = {'q' : 'get:new' + days_to_query + ':'+ settings.COUNTRY_CODE, 'p' : '1', 't' : 'ns', 'st' : 'adv'}

    response = JSONite(api_call(options))
    if response is None:
        return [None]

    netflix_titles = []
    for title in response['ITEMS']:
        netflix_titles.append(NetflixTitle(title))

    return netflix_titles

def countries_list():
    options = {'t': 'lc', 'q': 'available'}

    response = JSONite(api_call(options))
    if response is None:
        return [None]

    netflix_countries = []
    for country in response['ITEMS']:
        netflix_countries.append(tuple(country[:3]))

    return netflix_countries

def genres_list():
    options = {'t': 'genres'}

    response = JSONite(api_call(options))
    if response is None:
        return [None]

    netflix_genres = {}
    for genre in response['ITEMS']:
        netflix_genres = {**netflix_genres, **genre}

    return netflix_genres

def advanced_search(start_imdb_rating = '0', sort_by = 'Relevance', start_year = '1900',
                    genre_id = '0'):
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
    page = '1'
    clist = '400' # country
    query = '' # get:new10000
    imdb_votes = 'gt0' # gt[num] or lt[num]
    and_or = 'and'

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
                'p': page,
                'sa': and_or
                }

    response = JSONite(api_call(options))
    print(response)


if __name__ == '__main__':
    advanced_search()
