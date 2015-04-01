from server.library.api.constants import API_LIST
import urllib.request as request
import json


class LeagueOfLegends(object):
    """
        Wrapper to the official LoL Api (https://developer.riotgames.com/)
        It makes it more convenient to access various data
    """


def __init__(self, api_key, region='euw'):
    self.api_base_url = 'api.pvp.net/api/lol/'
    self.api_global_base_url = 'global.api.pvp.net'
    self.api_observer_url = '/observer-mode/rest/consumer/getSpectatorGameInfo/'
    self.api_key = api_key
    self.region = region


def _request(self, API, path, parameter):
    """ Returns a json coming from Riot's server API or our own cache if existing """
    if API not in API_LIST[API]:
        print('API NOT FOUND')
    # TODO: Improve the endpoint region to query to closest server to the user (not a priority tho)
    url = 'euw.' + self.api_base_url + self.region + '/v' + API_LIST[API] + '/' + API + '/' + request.quote(path)
    has_parameter = False
    if parameter:
        has_parameter = True
    url = url + ('&' if has_parameter else '?') + 'api_key=' + self.api_key
    print('url', url)
     #return json.loads(request.urlopen('http://euw.api.pvp.net/api/lol/' + self.regions + '?api_key=' + request.quote(self.api_key)).read())


def get_summoner(self, summoner_name):
    """ Returns a summoner given is 'summoner_name' """
    self._request('summoner', 'by-name' + summoner_name)
