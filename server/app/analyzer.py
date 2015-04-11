__author__ = 'Dewep'

from importlib import import_module
from general import log
from settings import ANALYZER_CLASSES


class AnalyzerBase(object):
    def analyze_player_as_an_ally(self, player):
        pass

    def analyze_player_as_an_enemy(self, player):
        pass

    def analyze_team_as_an_ally(self, team):
        pass

    def analyze_team_as_an_enemy(self, team):
        pass

    def analyze_game(self, game):
        pass


def get_analyzers():
    return _analyzers


def dialer_analyzers(instance, package, obj, is_ally=None):
    method = "analyze_" + package
    if is_ally is not None:
        method += "_as_an" + ("ally" if is_ally else "enemy")
    if hasattr(instance, method) and callable(instance.method):
        instance.method(obj)


_analyzers = []


for analyzer_class in ANALYZER_CLASSES:
    try:
        module_path, class_name = analyzer_class.rsplit('.', 1)
    except ValueError:
        log.error("Analyzer bad format: " + analyzer_class)
        continue
    try:
        module = import_module(module_path)
    except ImportError:
        log.error("Analyzer module not found: " + analyzer_class)
        continue
    try:
        analyzer = getattr(module, class_name)
    except AttributeError:
        log.error("Analyzer class not found: " + analyzer_class)
        continue
    try:
        instance_analyzer = analyzer()
        _analyzer.append(instance_analyzer)
    except TypeError:
        log.error("Analyzer is not callable: " + analyzer_class)
        continue
