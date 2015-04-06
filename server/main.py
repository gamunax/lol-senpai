from library.api.league_of_legends import LeagueOfLegends
from local_settings import API_KEY

lol_wrapper = LeagueOfLegends(API_KEY)
#lol_wrapper.get_summoner('Stegoo')
#lol_wrapper.get_match_history(20818053)
#lol_wrapper.get_champions()
#lol_wrapper.get_current_game_for_summoner(29481166)
#lol_wrapper.get_match_history(20818053)
#lol_wrapper.get_summoner_runes(20818053)
#lol_wrapper.get_summoner_masteries(20818053)
lol_wrapper.get_ranked_stats(20818053, '5')