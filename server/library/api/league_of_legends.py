from library.api.constants import API_LIST, REGIONAL_ENDPOINTS, SEASONS
from library.business.summoner import Summoner
from library.api import errors
import urllib.request as request
from cache import Cache
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

    def _request(self, api, path, params=None, cache_expire=600):
        """ Returns a json coming from Riot's server API or our own cache if existing """
        if api not in API_LIST:
            raise errors.UNKNOWN_API('Unknown API %s' % api)

        protocol_prefix = 'https://'
        if api == 'static-data':
            """ Requests to this API will not be counted to our Rate Limit"""
            url = (protocol_prefix + self.api_global_base_url + self.api_prefix + api + '/' + self.region + '/v'
                   + str(API_LIST.get(api)) + '/' + request.quote(path))
        elif api == 'current-game':
            url = (protocol_prefix + self.api_endpoint + '.' + self.api_base_url + self.api_observer_url
                   + request.quote(path))
        else:
            url = (protocol_prefix + self.api_endpoint + '.' + self.api_base_url + self.api_prefix + self.region + '/v'
                   + str(API_LIST.get(api)) + '/' + api + '/' + request.quote(path))
        url += '?'

        if params:
            # print('params', params)
            for key, value in params.items():
                url += key + '=' + value + '&'

        try:
            if Cache.get(url) is None:
                print('requesting url: ', url)
                data = request.urlopen(url + 'api_key=' + self.api_key).read().decode('utf-8')
                if data is not None:
                    Cache.set(url, data, ex=cache_expire)
            else:
                data = Cache.get(url)
            if data is not None:
                response = json.loads(data, strict=False)
                print('JSON DATA: ', response)
                return response
            return data
        except request.HTTPError as e:
            if e.code == 429:
                raise errors.RATE_LIMIT_EXCEEDED('Too many requests')
            elif e.code == 500 or e.code == 503:
                raise errors.SERVER_ERROR('Server error')
            else:
                raise errors.LoLSenpaiException('Bad request')
            return None

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

    def get_match_history(self, summoner_id):
        """ Returns the last 15 games for a given summoner """
        data = self._request('matchhistory', str(summoner_id))

    def get_summoner_runes(self, summoner_id):
        """ Returns the runes of a summoner """
        path = str(summoner_id) + '/runes'
        data = self._request('summoner', path)

    def get_summoner_masteries(self, summoner_id):
        """ Returns the masteries of a summoner """
        path = str(summoner_id) + '/masteries'
        data = self._request('summoner', path)

    def get_ranked_stats(self, summoner_id, season='3'):
        """ Rturns the ranked stats of a summoner for the given season (3,4,5) """
        if season not in SEASONS:
            raise errors.BAD_PARAMETER('Season not found %s' % season)
        path = 'by-summoner/' + str(summoner_id) + '/ranked'
        params = {'season': SEASONS[season]}
        data = self._request('stats', path, params)
