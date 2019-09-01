from datetime import timedelta, datetime
from settings import CACHE_FILE, CACHE_TTL, VERBOSE
import json

class CacheManager(object):
    '''
    Manager for old API requests stored in cache. The cache is queried through the manager at every API call.
    The cache is saved in the CACHE_FILE and updated with every new call made.
    Expired cache entries are invalidated every time an update is run.

    CacheManager is modeled after the Singleton desgin pattern and the instance should be fetched only through
    the getInstance static method.
    '''

    __instance = None

    def __init__(self) -> None:
        '''
        Loads cache from CACHE_FILE and implements Singleton pattern

        :raises: Exception
        :returns: None
        '''
        if CacheManager.__instance is None:
            CacheManager.__instance = self
            self.__entries = []
            self.__loadCache()
        else:
            raise Exception('Multiple instances created!')

    @staticmethod
    def getInstance() -> 'CacheManager':
        '''
        :returns: CacheManager instance
        :rtype: CacheManager
        '''
        if CacheManager.__instance is None:
            CacheManager()
        return CacheManager.__instance

    def __loadCache(self) -> None:
        '''
        Populates cache entries from file

        :returns: None
        '''
        entries_expired = 0

        try:
            content = open(CACHE_FILE, 'r').read()
        except FileNotFoundError:
            return

        lines = content.split('\n')[:-1]
        for i in range(0, len(lines), 4):
            timestamp = datetime.strptime(lines[i], '%Y-%m-%d %H:%M:%S')
            timeToLive = lines[i + 1]

            if timestamp + timedelta(seconds = int(timeToLive)) <= datetime.now():
                entries_expired += 1
                continue

            request = json.loads(lines[i + 2])
            response = json.loads(lines[i + 3])
            self.__entries.append(CacheEntry(request, response, timestamp = timestamp, timeToLive = int(timeToLive)))

        if entries_expired > 0:
            if VERBOSE:
                print("{} entries from cache expired".format(entries_expired))
            self.__updateCacheFile()

        if VERBOSE:
            print("Loaded {} entries from cache".format(len(self.__entries)))

    def loadFromCache(self, request: dict) -> dict:
        '''
        Checks for the given request in cache entries and returns its response if found else returns None

        :param request: query parameters for API call
        :type request: dict
        :returns: the API call's response if entry was cached, None otherwise
        :rtype: dict
        "
        '''

        entries_to_remove = []
        entries_expired = False
        return_value = None

        for entry in self.__entries:
            if entry.hasExpired():
                entries_to_remove.append(entry)
                entries_expired = True
                continue

            if entry.request == request:
                return_value = entry.response

        if VERBOSE and len(entries_to_remove) > 0:
            print("{} entries from cache expired".format(len(entries_to_remove)))

        for entry in entries_to_remove:
            self.__entries.remove(entry)
        if entries_expired:
            self.__updateCacheFile()

        if VERBOSE and return_value is not None:
            print("Loaded query response from cache")

        return return_value

    def saveToCache(self, request: dict, response: dict, timeToLive: int = CACHE_TTL) -> None:
        '''
        Adds a new entry to the cache and updates the cache file

        :param request: query parameters for API call
        :type request: dict

        :param response: API call's response
        :type response: dict

        :param timeToLive: cache entry's expire period
        :type timeToLive: int

        :returns: None
        '''
        newEntry = CacheEntry(request, response, timeToLive = timeToLive)
        self.__entries.append(newEntry)
        self.__saveToFile(newEntry)

    def __saveToFile(self, entry: 'CacheEntry') -> None:
        '''
        Saves the given entry in the CACHE_FILE

        :param entry: the cache entry to be saved
        :type entry: CacheEntry
        '''
        with open(CACHE_FILE, 'a') as f:
            f.write(entry.dateCreated.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(str(entry.timeToLive) + '\n')
            f.write(str(entry.request).replace("'", '"') + '\n')
            f.write(str(entry.response).replace("'", '"') + '\n')

    def __updateCacheFile(self) -> None:
        '''
        Updates CACHE_FILE with the current state of the entries

        :returns: None
        '''
        with open(CACHE_FILE, 'w') as f:
            for entry in self.__entries:
                f.write(entry.dateCreated.strftime('%Y-%m-%d %H:%M:%S') + '\n')
                f.write(str(entry.timeToLive) + '\n')
                f.write(str(entry.request).replace("'", '"') + '\n')
                f.write(str(entry.response).replace("'", '"') + '\n')

class CacheEntry(object):
    def __init__(self, request: dict, response: dict, timestamp: datetime = datetime.now(), timeToLive: int = CACHE_TTL) -> None:
        '''
        Creates a cache entry

        param request: query parameters for API call
        :type request: dict

        :param response: API call's response
        :type response: dict

        :param timeToLive: cache entry's expire period
        :type timeToLive: int

        :returns: None
        '''

        self.dateCreated = timestamp
        self.timeToLive = timeToLive
        self.response = response
        self.request = request

    def hasExpired(self) -> bool:
        '''
        :returns: boolean value on whether the entry has expired
        :rtype: bool 
        '''
        return self.dateCreated + timedelta(seconds = self.timeToLive) <= datetime.now()
