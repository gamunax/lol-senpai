__author__ = 'Dewep'


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
        # Fetch summoner
        # Abort if summoner not found
        # Fetch current game
        # Abort if not current game for this summoner
        # Abort if game's type is not supported
        # Construct teams (blue and purple)
        # Set the current summoner (+ make the method checking if it's an allie or not)
        pass

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
