from app.analyzer import AnalyzerBase
from app.advice import EnemyMissingRunesAdvice, EnemyNotMaxTierRunesAdvice


class AnalyzerRune(AnalyzerBase):

    def analyze_player_as_an_enemy(self, senpai, player):
        if player.runes.nb_missing_runes > 0:
            senpai.add_advice(senpai.PROS,
                              EnemyMissingRunesAdvice(player.get_champion().name, player.runes.nb_missing_runes))

        stats_not_max_tier = player.runes.get_nb_not_max_tier_runes()
        if stats_not_max_tier['red'] > 0 or stats_not_max_tier['blue'] > 0 \
                or stats_not_max_tier['yellow'] > 0 or stats_not_max_tier['black'] > 0:
            senpai.add_advice(senpai.PROS,
                              EnemyNotMaxTierRunesAdvice(player.get_champion().name, stats_not_max_tier))