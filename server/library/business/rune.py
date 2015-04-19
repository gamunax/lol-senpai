from general import get_wrapper
from flask.ext.babel import gettext, ngettext


class RunePage(object):
    def __init__(self, json_runes):
        self.max_runes = 30
        self.runes = []
        for rune in json_runes:
            if 'count' in rune:
                for x in range(0, rune['count']):
                    if 'runeId' in rune:
                        self.runes.append(get_wrapper().get_runes(rune['runeId']))
        self.nb_missing_runes = self.get_nb_missing_runes()
        self.nb_not_max_tier_runes = self.get_nb_not_max_tier_runes()

    def get_nb_missing_runes(self):
        return self.max_runes - len(self.runes)

    def get_nb_not_max_tier_runes(self):
        stats = {
            'red': 0,
            'yellow': 0,
            'blue': 0,
            'black': 0,
        }

        for rune in self.runes:
            if not rune.is_max_tier():
                stats[rune.type] += 1
        return stats

    def __str__(self):
        return 'This rune page has %d missing runes' % (self.nb_missing_runes)


class Rune(object):

    color_to_type = {
        'red': gettext('mark'),
        'yellow': gettext('seal'),
        'blue': gettext('glyph'),
        'black': gettext('quintessence'),
    }

    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.stats = json_data.get('stats')
        self.tags = json_data.get('tags')
        self.description = json_data.get('description')
        self.name = json_data.get('name')
        self.image = json_data.get('image')
        self.isRune = json_data.get('rune').get('isRune')
        self.tier = json_data.get('rune').get('tier')
        self.type = json_data.get('rune').get('type')
        self.type_name = self.color_to_type[self.type]

    def is_max_tier(self):
        return self.tier == "3"