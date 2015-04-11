from library.api.league_of_legends import LeagueOfLegends
from library.business.summoner import Summoner
from library.business.champion import Champion
from local_settings import API_KEY

lol_wrapper = LeagueOfLegends(API_KEY)
summoner = lol_wrapper.get_summoners('Tryndaminder')
print(summoner)
#lol_wrapper.get_match_history(summoner.id)
#champions = lol_wrapper.get_champions(72)
#print(champions[56])
lol_wrapper.get_current_game_for_summoner(summoner.id)
#lol_wrapper.get_match_history(20818053)
#lol_wrapper.get_summoner_runes(20818053)
#lol_wrapper.get_summoner_masteries(20818053)
#lol_wrapper.get_ranked_stats(20818053, '5')
