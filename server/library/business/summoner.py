from general import get_wrapper
from library.business.league import League
from library.business.rune import RunePage


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
            league = get_wrapper().get_league_info_for_summoner(self.id)
            self.leagues[queue] = League(league, self.region)
        if queue is not None:
            return self.leagues[queue]
        else:
            return self.leagues

    def is_me(self, id):
        return self.id == id


class Player(Summoner):
    def __init__(self, json_data, region):
        super().__init__(json_data, region)
        self.is_bot = json_data.get("bot")
        self.championId = json_data.get("championId")
        self.champion = None
        self.spell1Id = json_data.get("spell1Id")
        self.spell2Id = json_data.get("spell2Id")
        self.teamId = json_data.get("teamId")
        self.runes = RunePage(json_data.get('runes'))
        #print(self.runes)
        self.masteries = json_data.get('masteries')
        self.stats = json_data.get('stats')
        self.wards_placed = self.stats.get('wardsPlaced') if self.stats else None
        self.wards_killed = self.stats.get('wardsKilled') if self.stats else None
        self.vision_wards = self.stats.get('visionWardsBoughtInGame') if self.stats else None# Pink
        self.sight_wards = self.stats.get('sightWardsBoughtInGame') if self.stats else None # Green
        self.timeline = json_data.get('timeline')
        self.lane = self.timeline.get('lane') if self.timeline else None # MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM
        self.role = self.timeline.get('role') if self.timeline else None  # DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT
        if self.stats:
            if 'winner' in self.stats:
                self.left = False
                self.win = self.stats.get('winner')
            else:
                self.left = True

    def get_champion(self):
        if self.champion is None:
            self.champion = get_wrapper().get_champions(champion_id=self.championId)
        return self.champion

    def get_true_role(self):
        if self.lane == 'BOT' or self.lane == 'BOTTOM':
            if self.role == 'DUO_CARRY':
                return 'ADC'
            else:
                return 'SUPPORT'
        elif self.lane == 'MID' or self.lane == 'MID':
            return 'MID'
        elif self.lane == 'JUNGLE':
            return 'JUNGLE'
        else:
            return 'TOP'

    def __str__(self):
        return '%s, role: %s, lane: %s' % (self.get_champion().name, self.role, self.lane)