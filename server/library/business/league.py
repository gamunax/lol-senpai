class League(object):

    def __init__(self, json_data, region):
        self.region = region
        self.queue = json_data.get('queue')
        self.name = json_data.get('name')
        self.tier = json_data.get('tier')
        self.league_points = json_data.get('entries')[0].get('leaguePoints')
        self.mini_series = json_data.get('entries')[0].get('miniSeries')

    def is_in_promo(self):
        return True if self.mini_series else False