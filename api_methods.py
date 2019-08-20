import settings
from base import JSONite, api_call
from models.NetflixTitle import NetflixTitle

def new_releases(days_to_query = 7):
    options = {'q' : 'get:new7:'+ settings.COUNTRY_CODE, 'p' : '1', 't' : 'ns', 'st' : 'adv'}
    response = JSONite(api_call(options))

    netflix_titles = []
    for title in response['ITEMS']:
        netflix_titles.append(NetflixTitle(title))

    for title in netflix_titles:
        print(title)


if __name__ == '__main__':
    new_releases()
