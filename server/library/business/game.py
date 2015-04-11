from library.api.constants import MATCHMAKING_QUEUES, MAP_NAMES
from library.business.summoner import Player


class Game(object):

    def __init__(self, json_data, region):
        self.region = region
        self.gameId = json_data.get('gameId')
        self.gameLength = json_data.get('gameLength')
        self.gameMode = json_data.get('gameMode')
        self.gameStartTime = json_data.get('gameStartTime') or json_data.get('matchCreation')
        self.gameType = json_data.get('gameType')
        self.mapId = MAP_NAMES[json_data.get('mapId')]
        self.observers = json_data.get('observers')
        self.platformId = json_data.get('platformId')
        self.gameQueue = json_data.get('queueType') or MATCHMAKING_QUEUES[json_data.get('subType') or json_data.get('gameQueueConfigId')]
        self.players = list()
        self.blue_team = list()
        self.purple_team = list()
        for player in json_data.get('participants'):
            obj = Player(player, self.region)
            self.players.append(obj)
            if len(self.blue_team) == 0 or self.blue_team[0].teamId == obj.teamId:
                self.blue_team.append(obj)
            else:
                self.purple_team.append(obj)

    def is_ranked(self):
        return self.gameMode == "CLASSIC" and self.gameQueue[:7] == "RANKED_"

    def __lt__(self, other):
        return other.gameStartTime < self.gameStartTime


class CurrentGame(Game):

    class BannedChampions(object):
        def __init__(self, json_data):
            self.championId = json_data.get("championId")
            self.pickTurn = json_data.get("pickTurn")
            self.teamId = json_data.get("teamId")

    def __init__(self, json_data, region):
        super().__init__(json_data, region)
        self.bannedChampions = list()
        for champ in json_data.get('bannedChampions'):
            self.bannedChampions.append(self.BannedChampions(champ))

