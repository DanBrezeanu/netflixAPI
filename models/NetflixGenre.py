from settings import DB_SEP
from NetflixDatabase import NetflixDatabaseEntry
import html

class NetflixGenre(NetflixDatabaseEntry):
    def __init__(self, attrs: [str]) -> None:
        self.name, *self.netflixIDs = attrs
        self.name = html.unescape(self.name)
        
    def database_dump(self) -> str:
        return DB_SEP.join([self.name, *self.netflixIDs])
