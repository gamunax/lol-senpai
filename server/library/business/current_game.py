__author__ = 'Dewep'


from library.api.constants import MATCHMAKING_QUEUES, MAP_NAMES


class CurrentGame(object):

    class BannedChampions(object):
        def __init__(self, json_data):
            self.championId = json_data.get("championId")
            self.pickTurn = json_data.get("pickTurn")
            self.teamId = json_data.get("teamId")

    class Participants(object):
        class Mastery(object):
            def __init__(self, json_data):
                self.masteryId = json_data.get("masteryId")
                self.rank = json_data.get("rank")

        class Rune(object):
            def __init__(self, json_data):
                self.count = json_data.get("count")
                self.runeId = json_data.get("runeId")

        def __init__(self, json_data):
            self.is_bot = json_data.get("bot")
            self.championId = json_data.get("championId")
            self.profileIconId = json_data.get("profileIconId")
            self.spell1Id = json_data.get("spell1Id")
            self.spell2Id = json_data.get("spell2Id")
            self.summonerId = json_data.get("summonerId")
            self.summonerName = json_data.get("summonerName")
            self.teamId = json_data.get("teamId")
            self.runes = list()
            for rune in json_data.get('runes'):
                self.runes.append(self.Rune(rune))
            self.masteries = list()
            for mastery in json_data.get('masteries'):
                self.masteries.append(self.Mastery(mastery))

    def __init__(self, json_data):
        self.bannedChampions = list()
        for champ in json_data.get('bannedChampions'):
            self.bannedChampions.append(self.BannedChampions(champ))
        self.gameId = json_data.get('gameId')
        self.gameLength = json_data.get('gameLength')
        self.gameMode = json_data.get('gameMode')
        self.gameQueueConfigId = MATCHMAKING_QUEUES[json_data.get('gameQueueConfigId')]
        self.gameStartTime = json_data.get('gameStartTime')
        self.gameType = json_data.get('gameType')
        self.mapId = MAP_NAMES[json_data.get('mapId')]
        self.observers = json_data.get('observers')
        self.participants = list()
        for participant in json_data.get('participants'):
            self.participants.append(self.Participants(participant))
        self.platformId = json_data.get('platformId')

