from library.api.constants import MATCHMAKING_QUEUES, MAP_NAMES
from library.business.summoner import Participant


class Game(object):

    def __init__(self, json_data, region):
        self.region = region
        self.gameId = json_data.get('gameId')
        self.gameLength = json_data.get('gameLength')
        self.gameMode = json_data.get('gameMode')
        self.gameStartTime = json_data.get('gameStartTime')
        self.gameType = json_data.get('gameType')
        self.mapId = MAP_NAMES[json_data.get('mapId')]
        self.observers = json_data.get('observers')
        self.participants = list()
        for participant in json_data.get('participants'):
            self.participants.append(Participant(participant, self.region))
        self.platformId = json_data.get('platformId')


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
        self.gameQueueConfigId = MATCHMAKING_QUEUES[json_data.get('gameQueueConfigId')]

