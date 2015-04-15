from app.analyzer import AnalyzerBase
from app.data import get_info_summoner
from app.advice import AllyInPromoAdvice, EnemyInPromoAdvice


class AnalyzerSummoner(AnalyzerBase):
    def analyze_player_as_an_ally(self, senpai, player):
        stats = get_info_summoner(player.id, senpai.game.gameQueue)
        if stats['is_in_promo'] is True:
            senpai.add_advice(senpai.PROS, AllyInPromoAdvice(player.get_champion().name))

    def analyze_player_as_an_enemy(self, senpai, player):
        stats = get_info_summoner(player.id, senpai.game.gameQueue)
        if stats['is_in_promo'] is True:
            senpai.add_advice(senpai.CONS, EnemyInPromoAdvice(player.get_champion().name))