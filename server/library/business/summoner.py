from general import get_wrapper
from library.business.league import League

class Summoner(object):

    def __init__(self, json_data, region):
        self.id = json_data.get('id') or json_data.get("summonerId")
        self.name = json_data.get('name') or json_data.get("summonerName")
        self.region = region
        self.rune_pages = None
        self.leagues = {}

    def __str__(self):
        return '%s, id: %s, region: %s' % (self.name, str(self.id), self.region)

    def get_rune_pages(self):
        if self.rune_pages is None:
            self.rune_pages = get_wrapper().get_summoner_runes(self.id)
        return self.rune_pages

    def get_league_info(self, queue=None):
        if len(self.leagues) == 0:
            leagues = get_wrapper().get_league_info_for_summoner(self.id)
            for league in leagues:
                    self.leagues[league.get('queue')] = League(league, self.region)
        if queue is not None:
            return self.leagues[queue]
        else:
            return self.leagues


class Participant(Summoner):
    def __init__(self, json_data, region):
        super().__init__(json_data, region)
        self.is_bot = json_data.get("bot")
        self.championId = json_data.get("championId")
        self.champion = None
        self.spell1Id = json_data.get("spell1Id")
        self.spell2Id = json_data.get("spell2Id")
        self.teamId = json_data.get("teamId")
        self.runes = json_data.get('runes')
        self.masteries = json_data.get('masteries')

    def get_champion(self):
        if self.champion is None:
            self.champion = get_wrapper().get_champions(champion_id=self.championId)
        return self.champion
