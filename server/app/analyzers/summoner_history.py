from app.analyzer import AnalyzerBase
from app.data import get_stats_history_ranked
from flask.ext.babel import gettext, ngettext
from app.advice import EnemyLosingStreakAdvice, EnemyWinningStreakAdvice, EnemyPoorWardCoverageAdvice, \
    EnemyMainRoleAdvice, AllyWinningStreakAdvice


class AnalyzerSummonerHistory(AnalyzerBase):
    def analyze_player_as_an_ally(self, senpai, player):
        stats = get_stats_history_ranked(player.id, senpai.game.gameQueue)
        if stats['last_wins_in_a_row'] > 2:
            senpai.add_advice(senpai.PROS,
                              AllyWinningStreakAdvice(player.get_champion().name, stats['last_wins_in_a_row']))

    def analyze_player_as_an_enemy(self, senpai, player):
        # stats = {
        # 'game': 0,
        # 'left': 0,
        # 'last_wins_in_a_row': 0,
        # 'last_losses_in_a_row': 0,
        # 'loss': 0,
        # 'win': 0,
        # 'top': 0,
        # 'jungle': 0,
        # 'mid': 0,
        # 'adc': 0,
        # 'support': 0,
        # 'wards_placed': 0,
        # 'wards_killed': 0,
        # 'vision_wards': 0,
        # 'sight_wards': 0
        # }

        stats = get_stats_history_ranked(player.id, senpai.game.gameQueue)
        roles = {
            'top': stats['top'],
            'jungle': stats['jungle'],
            'mid': stats['mid'],
            'adc': stats['adc'],
            'support': stats['support'],
        }
        possible_main_role = max(roles, key=roles.get)
        main_role = possible_main_role if stats[possible_main_role] > (stats['game'] / 2 + 1) else None
        wards_per_game = stats['wards_placed'] / stats['game']
        # print('wards per game', wards_per_game, 'main_role', possible_main_role, main_role)
        if stats['last_losses_in_a_row'] > 2:
            senpai.add_advice(senpai.PROS,
                              EnemyLosingStreakAdvice(player.get_champion().name, stats['last_losses_in_a_row']))
        if stats['last_wins_in_a_row'] > 2:
            senpai.add_advice(senpai.CONS,
                              EnemyWinningStreakAdvice(player.get_champion().name, stats['last_wins_in_a_row']))
        if wards_per_game < 7 and main_role is not 'adc':
            senpai.add_advice(senpai.PROS, EnemyPoorWardCoverageAdvice(player.get_champion().name, wards_per_game))
        if main_role is not None:
            senpai.add_advice(senpai.INFO, EnemyMainRoleAdvice(player.get_champion().name, main_role))

