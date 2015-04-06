class Summoner(object):

    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.name = json_data.get('name')
        self.rune_pages = None

    def __str__(self):
        return '%s, id: %s' % (self.name, str(self.id))

    def set_rune_pages(self, data):
        self.rune_pages = data