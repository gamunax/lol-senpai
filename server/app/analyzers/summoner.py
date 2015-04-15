from app.analyzer import AnalyzerBase
from app.data import get_info_summoner


class AnalyzerSummoner(AnalyzerBase):
    def analyze_player_as_an_ally(self, senpai, player):
        stats = get_info_summoner(player.id, senpai.game.gameQueue)
        print("LAAAAAAAA", stats)