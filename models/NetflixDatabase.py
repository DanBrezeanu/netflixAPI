from models.NetflixTitle import NetflixTitle
from models.NetflixGenre import NetflixGenre
from datetime import datetime
from settings import PROJECT_ROOT, DATABASE_TABLE_SEP, DB_SEP
from base import log_error

class NetflixDatabase(object):
    __instance = None

    @staticmethod
    def getInstance():
        if NetflixDatabase.__instance is None:
            NetflixDatabase()
        return NetflixDatabase.__instance

    def __init__(self):
        if NetflixDatabase.__instance is None:
            NetflixDatabase.__instance = self
            self.__entries = []
            self.__file = PROJECT_ROOT + '/Database/database.netflix'
            self.__day_updated = None
            self.__buildDatabaseFromFile()
        else:
            raise Exception('Multiple instances created!')

    def __buildDatabaseFromFile(self):
        """
        title | netid | imagelink | synopsis | runtime | rating | type | released | genres
        """
        content = open(self.__file, 'r').read().split('\n')
        reading_titles = True

        try:
            self.__day_updated = datetime.strptime(content[0], '%Y-%m-%d %H:%M:%S')
        except (ValueError, IndexError):
            log_error("[WARN]  Date is not present in database or it has a wrong format")

        for line in content[1:-1]:
            reading_titles = False if line == DATABASE_TABLE_SEP else True
            self.__read_title(line) if reading_titles else self.__read_genre(line)

    def __read_title(self, line):
        elements = line.split(DB_SEP)
        self.__entries.append(NetflixTitle(elements[:-1]))

    def __read_genre(self, line):
        elements = line.split(DB_SEP)
        self.__genres.append(NetflixGenre(elements))

    def addEntry(self, entry):
        if isinstance(entry, NetflixTitle):
            self.__entries.append(entry)
        elif isinstance(entry, NetflixGenre):
            self.__genres.append(entry)
        else:
            log_error('[QUERY]  Cannot add given entry to the database')

    def removeEntry(self, entry):
        try:
            if isinstance(entry, NetflixTitle):
                self.__entries.remove(entry)
            elif isinstance(entry, NetflixGenre):
                self.__genres.remove(entry)
        except ValueError:
            log_error("[QUERY]  Entry not present in the database")



    def saveDatabaseToFile(self):
        with open(self.__file, 'w') as f:
            f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
            for entry in self.__entries:
                f.write(entry.database_dump() + '\n')
            f.write(DATABASE_TABLE_SEP + '\n')
            for genre in self.__genres:
                f.write(genre.database_dump() + '\n')
































        ##
