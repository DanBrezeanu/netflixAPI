from settings import DB_SEP
from typing import Union
from NetflixDatabase import NetflixDatabaseEntry

class NetflixTitle(NetflixDatabaseEntry):
    def __init__(self, attrs: Union[dict, list]) -> None:
        if isinstance(attrs, dict):
            self.__initalizeFromDict(attrs)
        elif isinstance(attrs, list):
            self.__initalizeFromList(attrs)

    def __initalizeFromDict(self, attrs: dict) -> None:
            self.netflixID = attrs['netflixid']
            self.title = attrs['title']
            self.image = attrs['image']
            self.synopsis = attrs['synopsis']
            self.rating = float(attrs['rating'])
            self.type = attrs['type']
            self.year_released = attrs['released']
            self.runtime = attrs['runtime']

    def __initalizeFromList(self, attrs: list) -> None:
            self.netflixID = attrs[1]
            self.title = attrs[0]
            self.image = attrs[2]
            self.synopsis = attrs[3]
            self.rating = float(attrs[5])
            self.type = attrs[6]
            self.year_released = attrs[7]
            self.runtime = attrs[4]

    def __str__(self):
        return  ' Title: ' + self.title       + '\n' + \
                ' ID   : ' + self.netflixID   + '\n' + \
                ' Image: ' + self.image       + '\n' + \
                ' Syn  : ' + self.synopsis    + '\n' + \
                ' Runtm: ' + self.runtime     + '\n' + \
                ' Ratng: ' + str(self.rating) + '\n'

    def __eq__(self, other):
        if isinstance(other, NetflixTitle):
            return self.netflixID == other.netflixID
        elif isinstance(other, str):
            return self.netflixID == other

    def database_dump(self) -> str:
        return DB_SEP.join([self.title, self.netflixID, self.image, self.synopsis, \
                            self.runtime, self.rating, self.type, self.year_released, '0'])


































#
