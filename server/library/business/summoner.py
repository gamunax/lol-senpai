class Summoner(object):

    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.name = json_data.get('name')
        self.region = json_data.get('region')
        self.rune_pages = None

    def __str__(self):
        return '%s, id: %s, region: %s' % (self.name, str(self.id), self.region)

    def get_rune_pages(self):
        from library.api.league_of_legends import LeagueOfLegends
        if self.rune_pages is None:
            lol_wrapper = LeagueOfLegends()
            self.rune_pages = lol_wrapper.get_summoner_runes(self.id)
        return self.rune_pages