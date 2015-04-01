from library.api.constants import API_LIST
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

    def _request(self, API, path, parameter=None):
        """ Returns a json coming from Riot's server API or our own cache if existing """
        if API not in API_LIST:
            print('API NOT FOUND')
        # TODO: Improve the endpoint region to query to closest server to the user (not a priority tho)
        url = 'https://euw.' + self.api_base_url + self.region + '/v' + str(API_LIST.get(API)) + '/' + API + '/' + request.quote(path)
        has_parameter = False
        if parameter:
            has_parameter = True
        url = url + ('&' if has_parameter else '?') + 'api_key=' + self.api_key
        print('url', url)
        data = request.urlopen(url).read()
        print('data', data)
        return data

    def get_summoner(self, summoner_name):
        """ Returns a summoner based on 'summoner_name' """
        data = self._request('summoner', 'by-name/' + summoner_name)

    def get_match_history(self, summoner_id):
        """ Returns a match history based on  'summoner_id' """
        data = self._request('matchhistory', summoner_id)