__author__ = 'Dewep'

from general import get_wrapper
from app.analyzer import get_analyzers, dialer_analyzers
from library.api.errors import LoLSenpaiException
from flask import abort


class SenpaiAdvices(object):
    PROS = 0
    CONS = 1
    INFO = 2

    def __init__(self, region, username):
        self.region = region
        self.username = username
        self.advices = {
            self.PROS: list(),
            self.CONS: list(),
            self.INFO: list()
        }
        self.game = None
        self.current_player = None

        self._initialise_game()
        self._analyze()

    def _initialise_game(self):
        lol_wrapper = get_wrapper(self.region)

        try:
            summoner = lol_wrapper.get_summoners(self.username)
        except LoLSenpaiException:
            summoner = None
            abort(404, {'message': 'Impossible to find this summoner.'})

        try:
            self.game = lol_wrapper.get_current_game_for_summoner(summoner.id)
        except LoLSenpaiException:
            abort(400, {'message': 'This summoner is not currently in a game.'})

        if not self.game.is_ranked():
            abort(400, {'message': 'Lol-Senpai works only for ranked games.'})

        for player in self.game.players:
            if player.id == summoner.id:
                self.current_player = player
                break

        self.is_blue_team = self.current_player.teamId == self.game.blue_team[0].teamId
        self.is_purple_team = self.current_player.teamId == self.game.purple_team[0].teamId

    def _analyze(self):
        for analyzer in get_analyzers():
            dialer_analyzers(analyzer, 'game', self, self.game)
            dialer_analyzers(analyzer, 'team', self, self.game.blue_team, self.is_blue_team)
            for player in self.game.blue_team:
                dialer_analyzers(analyzer, 'player', self, player, self.is_blue_team)
            dialer_analyzers(analyzer, 'team', self, self.game.purple_team, self.is_purple_team)
            for player in self.game.purple_team:
                dialer_analyzers(analyzer, 'player', self, player, self.is_purple_team)

    def get_advices(self, type_advice):
        return self.advices[type_advice]

    def add_advice(self, type_advice, message):
        self.advices[type_advice].append(message)

