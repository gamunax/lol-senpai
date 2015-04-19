from app.analyzer import AnalyzerBase
from app.advice import EnemyMissingRunesAdvice, EnemyNotTierMaxRunesAdvice


class AnalyzerRune(AnalyzerBase):

    def analyze_player_as_an_enemy(self, senpai, player):
        if player.runes.nb_missing_runes > 0:
            senpai.add_advice(senpai.PROS,
                              EnemyMissingRunesAdvice(player.get_champion().name, player.runes.nb_missing_runes))
        if player.runes.nb_not_tier_max_runes > 0:
            senpai.add_advice(senpai.PROS,
                              EnemyNotTierMaxRunesAdvice(player.get_champion().name, player.runes.nb_not_tier_max_runes))