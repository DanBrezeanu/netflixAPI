from datetime import datetime
from sys import stderr
import settings

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
            self.__file = settings.PROJECT_ROOT + '/Database/database.netflix'
            self.__day_updated = None
            self.buildDatabaseFromFile()
        else:
            raise Exception('Multiple instances created!')

    def buildDatabaseFromFile(self):
        """
        title | netid | imagelink | synopsis | runtime | rating | type | released | genres
        """
        content = open(self.__file, 'r').read()
        try:
            self.__day_updated = datetime.strptime(content[0], '%Y-%m-%d %H:%M:%S')
        except (ValueError, IndexError):
            print("[WARN]  Date is not present in database or it has a wrong format", file=stderr)

        for line in content[1:]:
            elements = line.split('|')
            self.__entries.append(NetflixTitle(elements[:-1]))

    def addTitle(self, title):
        self.__entries.append(title)

    def saveDatabaseToFile(self):
        with open(self.__file, 'w') as f:
            f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
            for entry in self.__entries:
                f.write(entry.database_dump() + '\n')
































        ##
