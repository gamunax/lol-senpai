from library.api.league_of_legends import LeagueOfLegends
from local_settings import API_KEY

lol_wrapper = LeagueOfLegends(API_KEY)
lol_wrapper.get_summoner('Stegoo')
lol_wrapper.get_match_history('20818053')

