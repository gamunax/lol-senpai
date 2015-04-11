from library.api.league_of_legends import LeagueOfLegends
from library.business.summoner import Summoner
from library.business.champion import Champion

lol_wrapper = LeagueOfLegends()
summoner = lol_wrapper.get_summoners('Stegoo')
summoner.get_rune_pages()
print(summoner.rune_pages)
#lol_wrapper.get_match_history(20818053)
#champions = lol_wrapper.get_champions(72)
#print(champions[56])
#lol_wrapper.get_current_game_for_summoner(29481166)
#lol_wrapper.get_match_history(20818053)
#lol_wrapper.get_summoner_runes(20818053)
#lol_wrapper.get_summoner_masteries(20818053)
#lol_wrapper.get_ranked_stats(20818053, '5')