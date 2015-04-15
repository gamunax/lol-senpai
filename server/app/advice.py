from flask.ext.babel import gettext, ngettext


class Advice(object):
    def get_message(self):
        pass

    def get_description(self):
        pass


class EnemyLosingStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_losses):
        self.champion_name = champion_name
        self.number_of_losses = number_of_losses

    def get_message(self):
        return gettext('The <span class="info enemy">enemy %(champion)s</span> is on a %(loss)d losing streak.',
                       champion=self.champion_name, loss=self.number_of_losses)

    def get_description(self):
        return gettext('Some players are prone to tilt and cannot think straight after a losing streak. '
                       'Try to focus them and take them down to ensure an easier win.')


class EnemyWinningStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_wins):
        self.champion_name = champion_name
        self.number_of_wins = number_of_wins

    def get_message(self):
        return gettext('The <span class="info enemy">enemy %(champion)s</span> is on a %(wins)d winning streak.',
                       champion=self.champion_name, wins=self.number_of_wins)

    def get_description(self):
        return gettext('A winning streak provides a boost of confidence.')


class EnemyPoorWardCoverageAdvice(Advice):
    def __init__(self, champion_name, wards_per_game):
        self.champion_name = champion_name
        self.wards_per_game = wards_per_game

    def get_message(self):
        return gettext('The <span class="info enemy">enemy %(champion)s</span> does not ward a lot. '
                       'He places %(wards_per_game)d wards per game on average.',
                       champion=self.champion_name, wards_per_game=self.wards_per_game)

    def get_description(self):
        return gettext('Vision is everything. A poor ward coverage means that this enemy is easier to gank and cannot '
                       'properly control objectives (dragon, nashor). They are in the dark most of the time.')


class EnemyNeverPlayedThisChampionAdvice(Advice):
    def __init__(self, champion_name):
        self.champion_name = champion_name

    def get_message(self):
        return gettext('The <span class="info enemy">enemy %(champion)s</span> has never played this champion before.',
                       champion=self.champion_name)

    def get_description(self):
        return gettext('')


class EnemyGoodWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, penta_kills, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.penta_kills = penta_kills
        self.played = played
        self.kda = kda

    def get_message(self):
        msg = gettext('The <span class="info enemy">enemy %(champion)s</span> is good with this champion '
                      '(%(percent_win).1f%% win ratio with %(kda).1f KDA over over %(played)d games).',
                      champion=self.champion_name, percent_win=self.percent_win, kda=self.kda, played=self.played)
        if self.penta_kills > 0:
            msg += gettext(' He has already done %(penta_kills)d penta kills with it', penta_kills=self.penta_kills)
        return msg

    def get_description(self):
        return gettext('')


class EnemyHasAGoodKDAWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, kda):
        self.champion_name = champion_name
        self.kda = kda

    def get_message(self):
        return gettext('"The <span class="info enemy">enemy %(champion)s</span> has a bad KDA with this champion (%(kda)f)',
                       champion=self.champion_name, kda=self.kda)

    def get_description(self):
        return gettext('')


class EnemyBadWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.played = played
        self.kda = kda

    def get_message(self):
        msg = gettext('The <span class="info enemy">enemy %(champion)s</span> is not very good with this champion '
                      '(%(percent_win).1f%% win ratio with %(kda).1f KDA over %(played)d games).',
                      champion=self.champion_name, percent_win=self.percent_win, kda=self.kda, played=self.played)
        return msg

    def get_description(self):
        return gettext('')


class EnemyMainRoleAdvice(Advice):
    def __init__(self, champion_name, role):
        self.champion_name = champion_name
        self.role = role

    def get_message(self):
        msg = gettext('The <span class="info enemy">enemy %(champion)s</span> probably mains '
                      '<span class="info enemy">%(role)s</span>.',
                      champion=self.champion_name, role=self.role)
        return msg

    def get_description(self):
        return gettext('')


class AllyGoodWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, penta_kills, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.penta_kills = penta_kills
        self.played = played
        self.kda = kda

    def get_message(self):
        msg = gettext('The <span class="info ally">allied %(champion)s</span> is good with this champion '
                      '(%(percent_win).1f%% win ratio with %(kda).1f KDA over %(played)d games).',
                      champion=self.champion_name, percent_win=self.percent_win, kda=self.kda, played=self.played)
        if self.penta_kills > 0:
            msg += gettext(' He has already done %(penta_kills)d penta kills with it', penta_kills=self.penta_kills)
        return msg

    def get_description(self):
        return gettext('')


class AllyWinningStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_wins):
        self.champion_name = champion_name
        self.number_of_wins = number_of_wins

    def get_message(self):
        return gettext('The <span class="info ally">allied %(champion)s</span> is on a %(wins)d winning streak.',
                       champion=self.champion_name, wins=self.number_of_wins)

    def get_description(self):
        return gettext('A winning streak provides a boost of confidence.')