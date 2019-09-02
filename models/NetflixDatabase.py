from models.NetflixTitle import NetflixTitle
from models.NetflixGenre import NetflixGenre
from datetime import datetime
from settings import PROJECT_ROOT, DATABASE_TABLE_SEP, DB_SEP
from base import log_error, runtime_to_minutes


class NetflixDatabase(object):
    __instance = None

    @staticmethod
    def getInstance() -> 'NetflixDatabase':
        if NetflixDatabase.__instance is None:
            NetflixDatabase()
        return NetflixDatabase.__instance


    def __init__(self) -> None:
        if NetflixDatabase.__instance is None:
            NetflixDatabase.__instance = self
            self.__entries = []
            self.__genres = []
            self.__file = PROJECT_ROOT + '/Database/database.netflix'
            self.__day_updated = None
            self.__buildDatabaseFromFile()
        else:
            raise Exception('Multiple instances created!')


    def __buildDatabaseFromFile(self) -> None:
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


    def __read_title(self, line: str) -> None:
        elements = line.split(DB_SEP)
        self.__entries.append(NetflixTitle(elements[:-1]))


    def __read_genre(self, line: str) -> None:
        elements = line.split(DB_SEP)
        self.__genres.append(NetflixGenre(elements))


    def addEntry(self, entry: 'NetflixDatabaseEntry') -> None:
        if isinstance(entry, NetflixTitle):
            self.__entries.append(entry)
        elif isinstance(entry, NetflixGenre):
            self.__genres.append(entry)
        else:
            log_error('[QUERY]  Cannot add given entry to the database')


    def removeEntry(self, entry: 'NetflixDatabaseEntry') -> None:
        try:
            if isinstance(entry, NetflixTitle):
                self.__entries.remove(entry)
            elif isinstance(entry, NetflixGenre):
                self.__genres.remove(entry)
        except ValueError:
            log_error("[QUERY]  Entry not present in the database")


    def query(self, q: 'Query') -> '[NetflixDatabaseEntry]':
        if not q.ok:
            return None

        if q.searchFor == 'title':
            return self.__queryTitles(q)
        else:
            return self.__queryGenres(q)

    def __queryTitles(self, q: 'Query') -> [NetflixTitle]:
        queriedEntries = []

        if q.netflixID is not None:
            if isinstance(q.netflixID, list):
                for entry in self.__entries:
                    for queriedEntry in q.netflixID:
                        if queriedEntry == entry:
                            queriedEntries.append(entry)
            else:
                queriedEntries = [self.__entries[self.__entries.index(q.netflixID)]]
        else:
            queriedEntries = self.__entries.copy()

        if q.ratingMin is not None:
            queriedEntries = list(filter(lambda x: x.ratingMin >= q.ratingMin, queriedEntries))

        if q.released is not None:
            queriedEntries = list(filter(lambda x: int(x.released) >= int(q.released), queriedEntries))

        if q.runtimeMax is not None:
            queriedEntries = list(filter(lambda x: runtime_to_minutes(x.runtimeMax) >= runtime_to_minutes(q.runtimeMax)))

        if q.titleMatching is not None:
            pass

        if q.synopsisMatching is not None:
            pass

        


    def __queryGenres(self, q: 'Query') -> [NetflixGenre]:
        # TODO:
        pass

    def saveDatabaseToFile(self) -> None:
        with open(self.__file, 'w') as f:
            f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
            for entry in self.__entries:
                f.write(entry.database_dump() + '\n')
            f.write(DATABASE_TABLE_SEP + '\n')
            for genre in self.__genres:
                f.write(genre.database_dump() + '\n')

class NetflixDatabaseEntry(object):
    def database_dump(self) -> str:
        return ''

class Query(object):
    def __init__(self, searchFor, netflixID = None, titleMatching = None, synopsisMatching = None,
                 ratingMin = None, released = None, runtimeMax = None, genreMatching = None,
                 genreIDs = None) -> None:
        self.searchFor        = searchFor
        self.netflixID        = netflixID
        self.titleMatching    = titleMatching
        self.synopsisMatching = synopsisMatching
        self.ratingMin        = ratingMin
        self.released         = released
        self.runtimeMax       = runtimeMax
        self.genreMatching    = genreMatching
        self.genreIDs         = genreIDs

        self.ok = self.__sanityCheck()

    def __sanityCheck(self) -> bool:
        ok = True

        if self.searchFor != "title" and self.searchFor != "genre":
            ok = False
            log_error("[ERROR] You can only search for 'title' or 'genre'")

        if self.netflixID is not None:
            if isinstance(self.netflixID, list):
                if not all(isinstance(x, str) for x in self.netflixID):
                    log_error('[ERROR] netflixID elements must have str type')
                    ok = False
            elif not isinstance(self.netflixID, str):
                    log_error('[ERROR] netflixID parameter must be either str or list')
                    ok = False

        if self.titleMatching is not None and not isinstance(self.titleMatching, str):
            log_error('[ERROR] titleMatching parameter must be str')
            ok = False

        if self.synopsisMatching is not None and not isinstance(self.synopsisMatching, str):
            log_error('[ERROR] synopsisMatching parameter must be str')
            ok = False

        if self.ratingMin is not None:
            if not isinstance(self.ratingMin, int) and not isinstance(self.rating, float):
                log_error('[ERROR] ratingMin parameter must be either int or float')
                ok = False
            elif float(self.ratingMin) < 0.0 or float(self.ratingMin) > 10.0:
                log_error('[ERROR] ratingMin parameter must have values between 0 and 10')
                ok = False
            else:
                self.ratingMin = float(self.ratingMin)

        if self.released is not None:
            try:
                self.released = int(self.released)
            except ValueError:
                log_error('[ERROR] wrong format for released parameter, must be int or str')
                ok = False

        if self.runtimeMax is not None:
            ok = False if runtime_to_minutes(self.runtimeMax) is None else ok

        if self.genreMatching is not None and not isinstance(self.genreMatching, str):
            log_error('[ERROR] genreMatching parameter must be str')
            ok = False

        if self.genreIDs is not None:
            if isinstance(self.genreIDs, list):
                if not all(isinstance(x, str) for x in self.genreIDs):
                    log_error('[ERROR] genreIDs elements must have str type')
                    ok = False
            elif not isinstance(self.genreIDs, str):
                    log_error('[ERROR] genreIDs parameter must be either str or list')
                    ok = False
        return ok
