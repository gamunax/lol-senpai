from flask.ext.babel import gettext, ngettext


class Advice(object):
    message = ""
    description = ""

    def get_message(self):
        return self.message

    def has_description(self):
        return self.description != ""

    def get_description(self):
        return self.description


class EnemyLosingStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_losses):
        self.champion_name = champion_name
        self.number_of_losses = number_of_losses
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> is on a %(loss)d losing streak.',
                               champion=self.champion_name, loss=self.number_of_losses)
        self.description = gettext('Some players are prone to tilt and cannot think straight after a losing streak. '
                                   'Try to focus them and take them down to ensure an easier win.')


class EnemyWinningStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_wins):
        self.champion_name = champion_name
        self.number_of_wins = number_of_wins
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> is on a %(wins)d winning streak.',
                               champion=self.champion_name, wins=self.number_of_wins)
        self.description = gettext('A winning streak provides a boost of confidence.')


class EnemyPoorWardCoverageAdvice(Advice):
    def __init__(self, champion_name, wards_per_game):
        self.champion_name = champion_name
        self.wards_per_game = wards_per_game
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> does not ward a lot. '
                               'He places %(wards_per_game)d wards per game on average.',
                               champion=self.champion_name, wards_per_game=self.wards_per_game)
        self.description = gettext('Vision is everything. A poor ward coverage means that this enemy is easier to gank and cannot '
                                   'properly control objectives (dragon, nashor). They are in the dark most of the time.')


class EnemyNeverPlayedThisChampionAdvice(Advice):
    def __init__(self, champion_name):
        self.champion_name = champion_name
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> has never played this champion before.',
                               champion=self.champion_name)


class EnemyGoodWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, penta_kills, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.penta_kills = penta_kills
        self.played = played
        self.kda = kda
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> is good with this champion '
                               '(%(percent_win).1f%% win ratio with %(kda).1f KDA over %(played)d games).',
                               champion=self.champion_name, percent_win=self.percent_win, kda=self.kda, played=self.played)
        if self.penta_kills > 0:
            self.message += gettext(' He has already done %(penta_kills)d penta kills with it', penta_kills=self.penta_kills)


class EnemyBadWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.played = played
        self.kda = kda
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> is not very good with this '
                               'champion (%(percent_win).1f%% win ratio with %(kda).1f KDA over %(played)d games).',
                               champion=self.champion_name, percent_win=self.percent_win, kda=self.kda,
                               played=self.played)


class EnemyMainRoleAdvice(Advice):
    def __init__(self, champion_name, role):
        self.champion_name = champion_name
        self.role = role
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> probably mains '
                               '<span class="info enemy">%(role)s</span>.',
                               champion=self.champion_name, role=self.role)


class EnemyLeftRecentlyAdvice(Advice):
    def __init__(self, champion_name, nb_left):
        self.champion_name = champion_name
        self.nb_left = nb_left
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> left a ranked game recently',
                               champion=self.champion_name)


class EnemyInPromoAdvice(Advice):
    def __init__(self, champion_name):
        self.champion_name = champion_name
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> is in a promotion series.',
                               champion=self.champion_name)


class EnemyMissingRunesAdvice(Advice):
    def __init__(self, champion_name, nb_missing_runes):
        self.champion_name = champion_name
        self.nb_missing_runes = nb_missing_runes
        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> '
                               'has %(nb_missing_runes)d missing runes',
                               champion=self.champion_name, nb_missing_runes=self.nb_missing_runes)


class EnemyNotMaxTierRunesAdvice(Advice):
    def __init__(self, champion_name, stats_not_max_tier):
        self.champion_name = champion_name
        self.stats_not_max_tier = stats_not_max_tier

        self.message = gettext('The <span class="info enemy">enemy %(champion)s</span> '
                               'has some tier 1 or 2 runes :',
                               champion=self.champion_name, nb_not_max_tier_runes=self.nb_not_max_tier_runes)

        if self.stats_not_max_tier['blue'] > 0:
            self.message += gettext(' %(count)d glyphs',
                                    count=self.stats_not_max_tier['blue'])
        if self.stats_not_max_tier['red'] > 0:
            self.message += gettext(' %(count)d marks',
                                    count=self.stats_not_max_tier['red'])
        if self.stats_not_max_tier['yellow'] > 0:
            self.message += gettext(' %(count)d seals',
                                    count=self.stats_not_max_tier['yellow'])
        if self.stats_not_max_tier['black'] > 0:
            self.message += gettext(' %(count)d quintessences',
                                    count=self.stats_not_max_tier['black'])


class AllyGoodWithThisChampionAdvice(Advice):
    def __init__(self, champion_name, percent_win, played, penta_kills, kda):
        self.champion_name = champion_name
        self.percent_win = percent_win
        self.penta_kills = penta_kills
        self.played = played
        self.kda = kda
        self.message = gettext('The <span class="info ally">allied %(champion)s</span> is good with this champion '
                               '(%(percent_win).1f%% win ratio with %(kda).1f KDA over %(played)d games).',
                               champion=self.champion_name, percent_win=self.percent_win, kda=self.kda,
                               played=self.played)
        if self.penta_kills > 0:
            self.message += gettext(' He has already done %(penta_kills)d penta kills with it',
                                    penta_kills=self.penta_kills)


class AllyWinningStreakAdvice(Advice):
    def __init__(self, champion_name, number_of_wins):
        self.champion_name = champion_name
        self.number_of_wins = number_of_wins
        self.message = gettext('The <span class="info ally">allied %(champion)s</span> is on a %(wins)d winning streak.',
                               champion=self.champion_name, wins=self.number_of_wins)
        self.description = gettext('A winning streak provides a boost of confidence.')


class AllyInPromoAdvice(Advice):
    def __init__(self, champion_name):
        self.champion_name = champion_name
        self.message = gettext('The <span class="info ally">allied %(champion)s</span> is in a promotion series.',
                               champion=self.champion_name)