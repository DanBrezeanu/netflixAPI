
class NetflixTitle(object):
    def __init__(self, attrs):
        self.netflixID = attrs['netflixid']
        self.title = attrs['title']
        self.image = attrs['image']
        self.synopsis = attrs['synopsis']
        self.rating = attrs['rating']
        self.type = attrs['type']
        self.year_released = attrs['released']
        self.runtime = attrs['runtime']

    def __str__(self):
        return ' Title: ' + self.title     + '\n' + \
               ' ID   : ' + self.netflixID + '\n' + \
               ' Image: ' + self.image     + '\n' + \
               ' Syn  : ' + self.synopsis  + '\n' + \
               ' Runtm: ' + self.runtime   + '\n' + \
               ' Ratng: ' + self.rating    + '\n'
