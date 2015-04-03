from library.api.constants import API_LIST, REGIONAL_ENDPOINTS
from library.business.summoner import Summoner
import urllib.request as request
import json


class LeagueOfLegends(object):
    """
        Wrapper to the official LoL Api (https://developer.riotgames.com/)
        It makes it more convenient to access various data
    """

    def __init__(self, api_key, region='euw'):
        self.api_base_url = 'api.pvp.net/'
        self.api_global_base_url = 'global.api.pvp.net/'
        self.api_prefix = 'api/lol/'
        self.api_observer_url = 'observer-mode/rest/consumer/getSpectatorGameInfo/'
        self.api_key = api_key
        self.api_endpoint = 'euw'  # Location of our server
        self.region = region
        self.platform_id = self._get_platform_id()

    def _request(self, API, path, params=None):
        """ Returns a json coming from Riot's server API or our own cache if existing """
        if API not in API_LIST:
            print('API NOT FOUND')

        protocol_prefix = 'https://'
        if API == 'static-data':
            """ Requests to this API will not be counted to our Rate Limit"""
            url = protocol_prefix + self.api_global_base_url + self.api_prefix + API + '/' + self.region + '/v' + str(API_LIST.get(API)) + '/' + \
                  request.quote(path)
        elif API == 'current-game':
            url = protocol_prefix + self.api_endpoint + '.' + self.api_base_url + self.api_observer_url + request.quote(path)
        else:
            url = protocol_prefix + self.api_endpoint + '.' + self.api_base_url + self.api_prefix + self.region + '/v' + str(API_LIST.get(API)) + '/' + API + '/' + \
                  request.quote(path)
        url += '?'

        if params:
            # print('params', params)
            for key, value in params.items():
                url += key + '=' + value + '&'
        url += 'api_key=' + self.api_key
        print('requesting url: ', url)
        data = request.urlopen(url).read().decode('utf-8')
        if data is not None:
            response = json.loads(data, strict=False)
            print('JSON DATA: ', response)
            return response
        return data

    def _get_platform_id(self):
        if self.region not in REGIONAL_ENDPOINTS:
            raise ValueError()
        return REGIONAL_ENDPOINTS.get(self.region)

    def get_summoner(self, summoner_name):
        """ Returns a summoner based on 'summoner_name' """
        data = self._request('summoner', 'by-name/' + summoner_name)
        # print(data.get(summoner_name.lower()))

    def get_match_history(self, summoner_id):
        """ Returns a match history based on  'summoner_id' """
        data = self._request('matchhistory', str(summoner_id))

    def get_champions(self, champion_id=None, params={'champData': 'tags'}):
        """ Returns the list of champions or info about a specific champion """
        path = 'champion' + ('/' + str(champion_id) if champion_id else '')
        data = self._request('static-data', path, params)

    def get_current_game_for_summoner(self, summoner_id):
        path = self.platform_id + '/' + str(summoner_id)
        data = self._request('current-game', path)