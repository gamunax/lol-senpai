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
        'last_wins_in_a_row': 0,
        'last_losses_in_a_row': 0,
        'loss': 0,
        'win': 0,
        'top': 0,
        'jungle': 0,
        'mid': 0,
        'adc': 0,
        'support': 0,
        'wards_placed': 0,
        'wards_killed': 0,
        'vision_wards': 0,
        'sight_wards': 0
    }

    data = []
    for i in range(0, batch):
        data += lol_wrapper.get_match_history(summoner_id, ranked_queue, len(data))

    # print('nb result', len(data))
    win_in_a_row = 0
    loss_in_a_row = 0
    for game in sorted(data):
        print(datetime.datetime.fromtimestamp(game.gameStartTime / 1e3).strftime('%Y-%m-%d %H:%M:%S'))
        for player in game.blue_team:
            print('__________BLUE______', player)
            stats['wards_placed'] += player.wards_placed
            stats['wards_killed'] += player.wards_killed
            stats['vision_wards'] += player.vision_wards
            stats['sight_wards'] += player.sight_wards
            stats[player.get_true_role().lower()] += 1
            stats['game'] += 1
            if hasattr(player, 'win'):
                if player.win:
                    stats['win'] += 1
                    if stats['last_wins_in_a_row'] == 0 and win_in_a_row >= 0:
                        win_in_a_row += 1
                        if loss_in_a_row > 0:
                            stats['last_losses_in_a_row'] = loss_in_a_row
                            loss_in_a_row = -1
                else:
                    stats['loss'] += 1
                    if stats['last_losses_in_a_row'] == 0 and loss_in_a_row >= 0:
                        loss_in_a_row += 1
                        if win_in_a_row > 0:
                            stats['last_wins_in_a_row'] = win_in_a_row
                            win_in_a_row = -1

            if player.left:
                stats['left'] += 1

    print(stats)
    return stats
