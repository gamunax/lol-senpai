from general import get_wrapper
from app.senpai import get_stats_champion_ranked

# Find a summoner in a game : http://www.lolnexus.com/recent-games?filter-region=2&filter-queue-type=2&filter-sort=1

lol_wrapper = get_wrapper()
summoner = lol_wrapper.get_summoners('AurelienM')
print(summoner)
print(get_stats_champion_ranked(summoner.id, 59))
# lol_wrapper.get_match_history(summoner.id)
# champions = lol_wrapper.get_champions(72)
# print(champions[56])
# lol_wrapper.get_current_game_for_summoner(summoner.id)
# lol_wrapper.get_match_history(20818053)
# lol_wrapper.get_summoner_runes(20818053)
# lol_wrapper.get_summoner_masteries(20818053)
# lol_wrapper.get_ranked_stats(20818053, '5')
