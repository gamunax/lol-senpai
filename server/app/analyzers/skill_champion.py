__author__ = 'Dewep'

from app.analyzer import AnalyzerBase
from app.data import get_stats_champion_ranked
from app.advice import EnemyNeverPlayedThisChampionAdvice, EnemyGoodWithThisChampionAdvice, \
    EnemyHasAGoodKDAWithThisChampionAdvice, EnemyBadWithThisChampionAdvice, AllyGoodWithThisChampionAdvice


class AnalyzerSkillChampion(AnalyzerBase):
    def analyze_player_as_an_ally(self, senpai, player):
        stats = get_stats_champion_ranked(player.id, player.championId)
        if stats['played'] > 3 and stats['percent_win'] > 70:
            senpai.add_advice(senpai.PROS, AllyGoodWithThisChampionAdvice(player.get_champion().name,
                                                                          stats['percent_win'], stats['played'], stats['pentaKills'], stats['kda']))

    def analyze_player_as_an_enemy(self, senpai, player):
        stats = get_stats_champion_ranked(player.id, player.championId)
        if stats is None:
            senpai.add_advice(senpai.PROS, EnemyNeverPlayedThisChampionAdvice(player.get_champion().name))
        elif stats['kda'] < 1:
            senpai.add_advice(senpai.PROS, EnemyHasAGoodKDAWithThisChampionAdvice(player.get_champion().name, stats['kda']))
        elif stats['played'] > 3 and stats['percent_win'] > 70:
            senpai.add_advice(senpai.CONS, EnemyGoodWithThisChampionAdvice(player.get_champion().name,
                                                                           stats['percent_win'], stats['played'], stats['pentaKills'], stats['kda']))
        elif stats['played'] > 3 and stats['percent_win'] < 30:
            senpai.add_advice(senpai.PROS, EnemyBadWithThisChampionAdvice(player.get_champion().name,
                                                                          stats['percent_win'], stats['played'], stats['kda']))
