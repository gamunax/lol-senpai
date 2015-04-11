from general import get_wrapper, function_logger
import datetime

lol_wrapper = get_wrapper()


@function_logger
def get_stats_champion_ranked(summoner_id, champion_id=0):
    data = lol_wrapper.get_ranked_stats(summoner_id)
    for champ in data.get('champions'):
        if champ.get('id') == champion_id:
            stats = champ.get('stats')
            kda = -1
            if stats.get('totalDeathsPerSession') > 0:
                kda = stats.get('totalChampionKills') + stats.get('totalAssists')
                kda = round(kda / stats.get('totalDeathsPerSession'), 2)
            return {
                'quadraKills': stats.get('totalQuadraKills'),
                'pentaKills': stats.get('totalPentaKills'),
                'lost': stats.get('totalSessionsLost'),
                'won': stats.get('totalSessionsWon'),
                'kills': stats.get('totalChampionKills'),
                'assits': stats.get('totalAssists'),
                'deaths': stats.get('totalDeathsPerSession'),
                'played': stats.get('totalSessionsPlayed'),
                'kda': kda,
                'percent_win': round(stats.get('totalSessionsWon') * 100 / stats.get('totalSessionsPlayed'), 2)
            }
    return None


@function_logger
def get_stats_history_ranked(summoner_id, ranked_queue=None, batch=2):
    stats = {
        'game': 0,
        'left': 0,
        'loss': 0,
        'loss_in_a_row': 0,
        'win': 0,
        'win_in_a_row': 0,
        'top': 0,
        'jungle': 0,
        'mid': 0,
        'adc': 0,
        'support': 0
    }

    data = []
    for i in range(0, batch):
        data += lol_wrapper.get_match_history(summoner_id, ranked_queue, len(data))

    print(len(data))
    for game in sorted(data):
        print(datetime.datetime.fromtimestamp(game.gameStartTime / 1e3).strftime('%Y-%m-%d %H:%M:%S'))
        for player in game.blue_team:
            print('__________BLUE______', player)
            stats[player.get_true_role().lower()] += 1
            stats['game'] += 1
            if hasattr(player, 'win'):
                if player.win:
                    stats['win'] += 1
                else:
                    stats['loss'] += 1

            if player.left:
                stats['left'] += 1

    print(stats)
    return stats
