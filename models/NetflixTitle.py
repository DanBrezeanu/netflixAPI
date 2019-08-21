
class NetflixTitle(object):
    def __init__(self, attrs):
        if isinstance(attrs, dict):
            self.__initalizeFromDict(attrs)
        elif isinstance(attrs, list):
            self.__initalizeFromList(attrs)

    def __initalizeFromDict(self, attrs):
            self.netflixID = attrs['netflixid']
            self.title = attrs['title']
            self.image = attrs['image']
            self.synopsis = attrs['synopsis']
            self.rating = attrs['rating']
            self.type = attrs['type']
            self.year_released = attrs['released']
            self.runtime = attrs['runtime']

    def __initalizeFromList(self, attrs):
            self.netflixID = attrs[1]
            self.title = attrs[0]
            self.image = attrs[2]
            self.synopsis = attrs[3]
            self.rating = attrs[5]
            self.type = attrs[6]
            self.year_released = attrs[7]
            self.runtime = attrs[4]

    def __str__(self):
        return  ' Title: ' + self.title     + '\n' + \
                ' ID   : ' + self.netflixID + '\n' + \
                ' Image: ' + self.image     + '\n' + \
                ' Syn  : ' + self.synopsis  + '\n' + \
                ' Runtm: ' + self.runtime   + '\n' + \
                ' Ratng: ' + self.rating    + '\n'

    def database_dump(self):
        return self.title    + '|' + self.netflixID     + '|' + self.image  + '|' + \
               self.synopsis + '|' + self.runtime       + '|' + self.rating + '|' + \
               self.type     + '|' + self.year_released + '|' + '0'



































#
