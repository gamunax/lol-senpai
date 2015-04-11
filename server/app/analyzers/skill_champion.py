__author__ = 'Dewep'

from app.analyzer import AnalyzerBase
from app.data import get_stats_champion_ranked


class AnalyzerSkillChampion(AnalyzerBase):
    def analyze_player_as_an_ally(self, senpai, player):
        senpai.add_advice(senpai.INFO, player.get_champion().name + " is in your team")

    def analyze_player_as_an_enemy(self, senpai, player):
        senpai.add_advice(senpai.INFO, player.get_champion().name + " is not in your team")
        stats = get_stats_champion_ranked(player.id, player.championId)
        if stats is None:
            senpai.add_advice(senpai.PROS, "The enemy team %s has never played this champion before" % player.champion.name)
        elif stats['kda'] < 1:
            senpai.add_advice(senpai.PROS, "The enemy team %s has a bad KDA with this champion (%f)" % (player.champion.name, stats['kda']))
        elif stats['played'] > 3 and stats['percent_win'] > 70:
            senpai.add_advice(senpai.CONS, "The enemy team %s is good with this champion (%f%% win ratio)" % (player.champion.name, stats['percent_win']))
        elif stats['pentaKills'] > 0:
            senpai.add_advice(senpai.CONS, "The enemy team %s is good with this champion, he has been already done %d pentakills with him" % (player.champion.name, stats['pentaKills']))
