from library.business.summoner import Summoner
from library.business.champion import Champion
from library.business.game import CurrentGame, Game
from library.business.rune import Rune
from library.api.constants import API_LIST, REGIONAL_ENDPOINTS, SEASONS, LOCALES
from library.api import errors
import urllib.request as request
from general import log, Cache
from settings import API_KEY
from flask import g

import json


class LeagueOfLegends(object):
    """
        Wrapper to the official LoL Api (https://developer.riotgames.com/)
        It makes it more convenient to access various data
    """

    def __init__(self, region='euw'):
        self.api_base_url = 'api.pvp.net/'
        self.api_global_base_url = 'global.api.pvp.net/'
        self.api_prefix = 'api/lol/'
        self.api_observer_url = 'observer-mode/rest/consumer/getSpectatorGameInfo/'
        self.api_key = API_KEY
        self.api_endpoint = region  # Location of our server
        self.region = region
        self.platform_id = self._get_platform_id()

    def _request(self, api, path, params=None, cache_expire=60*15):
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
            for key, value in params.items():
                url += key + '=' + value + '&'

        try:
            if Cache.get(url) is None:
                log.info('requesting url: %s' % url)
                data = request.urlopen(url + 'api_key=' + self.api_key).read()
                if data is not None:
                    Cache.set(url, data, ex=cache_expire)
            else:
                data = Cache.get(url)
            data = data.decode('iso-8859-1')
            if data is not None:
                response = json.loads(data, strict=False)
                log.debug('JSON DATA: ' + json.dumps(response, indent=4))
                return response
            return data
        except request.HTTPError as e:
            log.error("HTTPError " + str(e.code) + ": " + str(e))
            if e.code == 429:
                raise errors.RATE_LIMIT_EXCEEDED('Too many requests')
            elif e.code == 500 or e.code == 503:
                raise errors.SERVER_ERROR('Server error')
            else:
                raise errors.LoLSenpaiException('Bad request')

    def _get_platform_id(self):
        if self.region not in REGIONAL_ENDPOINTS:
            raise ValueError()
        return REGIONAL_ENDPOINTS.get(self.region)

    def get_summoners(self, summoner_names):
        """ Returns a summoner list based on 'summoner_names' """
        is_list = False
        if isinstance(summoner_names, list):
            is_list = True
            summoner_names = ','.join(summoner_names)
        data = self._request('summoner', 'by-name/' + summoner_names, cache_expire=60*60*24*7)

        if is_list:
            summoners = {}
            for user in data:
                summoner = Summoner(data[user], self.region)
                summoners[summoner.id] = summoner
            return summoners
        else:
            for user in data:
                return Summoner(data[user], self.region)

    def get_summoner_runes(self, summoner_id):
        """ Returns runes of a summoner  'summoner_id' """
        data = self._request('summoner', str(summoner_id) + '/runes')
        return data.get(str(summoner_id)).get('pages')

    def get_runes(self, rune_id=None, rune_data='all'):
        """ Returns info about the rune 'rune_id' """
        # https://global.api.pvp.net/api/lol/static-data/euw/v1.2/rune/5273?runeData=all&api_key=fcb32d30-62c9-4888-a299-0596441978f8
        # https://global.api.pvp.net/api/lol/static-data/euw/v1.2/rune?api_key=fcb32d30-62c9-4888-a299-0596441978f8
        path = 'rune' + ('/' + str(rune_id) if rune_id else '')
        params = {
            'runeData': rune_data,
            'locale': LOCALES[g.lang]
        }
        data = self._request('static-data', path, params, cache_expire=60*60*24*7)
        if rune_id:
            return Rune(data)
        return None

    def get_match_history(self, summoner_id, ranked_queue='RANKED_SOLO_5x5', begin_index=0, end_index=None):
        """ Returns a match history based on  'summoner_id' """
        params = {'rankedQueues': ranked_queue}
        if begin_index is not None:
            params['beginIndex'] = str(begin_index)
        if end_index is not None:
            params['endIndex'] = str(end_index)
        data = self._request('matchhistory', str(summoner_id), params, cache_expire=60*30)
        games = []
        for game in data.get('matches'):
            games.append(Game(game, self.region))
        return games

    def get_champions(self, champion_id=None, champ_data='all'):
        """ Returns the list of champions or info about a specific champion """
        path = 'champion' + ('/' + str(champion_id) if champion_id else '')
        params = {
            'champData': champ_data,
            'locale': LOCALES[g.lang]
        }
        data = self._request('static-data', path, params, cache_expire=60*60*24*7)
        if champion_id:
            return Champion(data)
        else:
            data = data.get('data')
            champions = {}
            for champ in data:
                champion = Champion(data[champ])
                champions[champion.id] = champion
            return champions

    #https://global.api.pvp.net/api/lol/static-data/euw/v1.2/rune?runeListData=stats&api_key=fcb32d30-62c9-4888-a299-0596441978f8
    def get_current_game_for_summoner(self, summoner_id):
        path = self.platform_id + '/' + str(summoner_id)
        data = self._request('current-game', path, cache_expire=60)
        return CurrentGame(data, self.region)

    def get_ranked_stats(self, summoner_id, season='5'):
        """ Returns the ranked stats of a summoner for the given season (3,4,5) """
        if season not in SEASONS:
            raise errors.BAD_PARAMETER('Season not found %s' % season)
        path = 'by-summoner/' + str(summoner_id) + '/ranked'
        params = {'season': SEASONS[season]}
        data = self._request('stats', path, params, cache_expire=60*60*4)
        return data

    def get_summary_stats(self, summoner_id, season='5'):
        """ Returns the summary stats of a summoner for the given season (3,4,5) """
        if season not in SEASONS:
            raise errors.BAD_PARAMETER('Season not found %s' % season)
        path = 'by-summoner/' + str(summoner_id) + '/summary'
        params = {'season': SEASONS[season]}
        data = self._request('stats', path, params, cache_expire=60*60*4)
        return data

    def get_league_info_for_summoner(self, summoner_id, ranked_queue='RANKED_SOLO_5x5'):
        path = 'by-summoner/' + str(summoner_id) + '/entry'
        data = self._request('league', path).get(str(summoner_id))
        for stat in data:
            if stat.get('queue') == ranked_queue:
                return stat
        return None


class LeagueOfLegendsImage(object):
    @staticmethod
    def get_base_url():
        return 'http://ddragon.leagueoflegends.com/cdn/' + API_LIST.get('image') + '/' + '/img/'
