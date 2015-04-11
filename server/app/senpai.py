__author__ = 'Dewep'


from general import get_wrapper
from library.api.errors import LoLSenpaiException
from flask import abort


class SenpaiAdvices(object):
    PROS = 0
    CONS = 1
    INFOS = 2

    def __init__(self, region, username):
        self.region = region
        self.username = username
        self.advices = {
            self.PROS: list(),
            self.CONS: list(),
            self.INFOS: list()
        }
        self.game = None
        self.current_summoner = None

        self._initialise_game()
        self._analyse()

    def _initialise_game(self):
        lol_wrapper = get_wrapper()

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

        # Construct teams (blue and purple)
        # Set the current summoner (+ make the method checking if it's an allie or not)

    def _analyse(self):
        # Loop on teams
        # Loop on players
        # Loop on analysers
        pass

    def get_advices(self, type_advice):
        return self.advices[type_advice]

    def add_advice(self, type_advice, message):
        self.advices[type_advice].append(message)


_analyser = []


def register_analyser():
    def decorator(f):
        _analyser.append(f)
        return f
    return decorator
