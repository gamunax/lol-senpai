from general import get_wrapper, function_logger


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
def get_stats_history_ranked(summoner_id, ranked_queue= None):
    data = lol_wrapper.get_match_history(summoner_id)
    stats = {
        'left_games' : 0,
        'loss': 0,
        'loss_in_a_row': 0,
        'win': 0,
        'win_in_a_row': 0
    }
    for game in data:
        print('________________', game)

    return stats
