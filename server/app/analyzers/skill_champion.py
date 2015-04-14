__author__ = 'Dewep'

from app.analyzer import AnalyzerBase
from app.data import get_stats_champion_ranked
from app.advice import EnemyNeverPlayedThisChampionAdvice, EnemyGoodWithThisChampionAdvice, \
    EnemyHasAGoodKDAWithThisChampionAdvice


class AnalyzerSkillChampion(AnalyzerBase):
    #def analyze_player_as_an_ally(self, senpai, player):
        #print('test')
        # senpai.add_advice(senpai.INFO, player.get_champion().name + " is in your team")

    def analyze_player_as_an_enemy(self, senpai, player):
        # senpai.add_advice(senpai.INFO, player.get_champion().name + " is not in your team")
        stats = get_stats_champion_ranked(player.id, player.championId)
        if stats is None:
            senpai.add_advice(senpai.PROS, EnemyNeverPlayedThisChampionAdvice(player.get_champion().name))
        elif stats['kda'] < 1:
            senpai.add_advice(senpai.PROS, EnemyHasAGoodKDAWithThisChampionAdvice(player.get_champion().name, stats['kda']))
        elif stats['played'] > 3 and stats['percent_win'] > 70:
            senpai.add_advice(senpai.CONS, EnemyGoodWithThisChampionAdvice(player.get_champion().name, stats['percent_win'], stats['pentaKills']))
