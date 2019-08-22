
class NetflixGenre(object):
    def __init__(self, attrs):
        self.name, *self.netflixIDs = attrs

    def database_dump(self):
        return '|'.join([self.name, *self.netflixIDs])
