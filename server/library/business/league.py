from library.api.constants import DIVISIONS, TIERS

class League(object):

    def __init__(self, json_data, region):
        self.region = region
        self.queue = json_data.get('queue')
        self.name = json_data.get('name')
        self.tier = json_data.get('tier')
        self.league_points = json_data.get('entries')[0].get('leaguePoints')
        self.division = json_data.get('entries')[0].get('division')
        self.mini_series = json_data.get('entries')[0].get('miniSeries')

    def is_in_promo(self):
        return True if self.mini_series else False

    def get_info_about_promo(self):
        if self.mini_series:
            return {
                'wins': self.mini_series.get('wins'),
                'losses': self.mini_series.get('losses'),
                'target': self.mini_series.get('target'),
                'progress': self.mini_series.get('progress')
            }
        return None

    def get_next_league(self):
        current_index_tier = TIERS.index(self.tier)
        current_index_division = DIVISIONS.index(self.division)
        next_tier = self.tier if self.division != 'I' else TIERS[(current_index_tier + 1) % len(TIERS)]
        next_division = DIVISIONS[(current_index_division + 1) % len(DIVISIONS)]
        # print('tier', self.tier, 'division', self.division, 'next_tier', next_tier, 'next_division', next_division)
        return {
            'division': next_division,
            'tier': next_tier
        }