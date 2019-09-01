from settings import DB_SEP

class NetflixGenre(object):
    def __init__(self, attrs: [str]) -> None:
        self.name, *self.netflixIDs = attrs

    def database_dump(self) -> str:
        return DB_SEP.join([self.name, *self.netflixIDs])
