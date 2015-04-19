class Champion(object):

    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.name = json_data.get('name')
        self.key = json_data.get('key')
        self.tags = json_data.get('tags')
        self.image = json_data.get('image')
        self.image_url = self.get_image_url()
        self.partype = json_data.get('partype') #None, Mana, BloodWell, Battlefury, Energy, Heat, Shield

    def __str__(self):
        return '%s, id: %s, tags: %s, image: %s' % (self.name, str(self.id), self.tags, self.image_url)

    def get_image_url(self, size='square'):
        """ Returns the image url from data dragon (static data) """
        from library.api.league_of_legends import LeagueOfLegendsImage

        url = LeagueOfLegendsImage.get_base_url() + 'champion/'
        if size == 'splash':
            url += 'splash/'
        elif size == 'loading':
            url += 'loading/'
        return url + self.image.get('full')