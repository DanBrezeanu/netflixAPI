from settings import DB_SEP

class NetflixGenre(object):
    def __init__(self, attrs):
        self.name, *self.netflixIDs = attrs

    def database_dump(self):
        return DB_SEP.join([self.name, *self.netflixIDs])
