import os
import battlenet
from operator import itemgetter

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

class DataTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

    def test_races(self):
        races = self.connection.get_character_races(battlenet.UNITED_STATES)

        self.assertEqual({
            1: 'Human',
            2: 'Orc',
            3: 'Dwarf',
            4: 'Night Elf',
            5: 'Undead',
            6: 'Tauren',
            7: 'Gnome',
            8: 'Troll',
            9: 'Goblin',
            10: 'Blood Elf',
            11: 'Draenei',
            22: 'Worgen',
            24: 'Pandaren',
            25: 'Pandaren',
            26: 'Pandaren',
        }, dict([(race.id, race.name) for race in races]))

        for race in races:
            self.assertIn(race.side, ['alliance', 'horde', 'neutral'])

    def test_classes(self):
        classes = self.connection.get_character_classes(
            battlenet.UNITED_STATES, raw=True)

        classes_ = [{
            'powerType': 'focus',
            'mask': 4,
            'id': 3,
            'name': 'Hunter'
        }, {
            'powerType': 'energy',
            'mask': 8,
            'id': 4,
            'name': 'Rogue'
        }, {
            'powerType': 'rage',
            'mask': 1,
            'id': 1,
            'name': 'Warrior'
        }, {
            'powerType': 'mana',
            'mask': 2,
            'id': 2,
            'name': 'Paladin'
        }, {
            'powerType': 'mana',
            'mask': 64,
            'id': 7,
            'name': 'Shaman'
        }, {
            'powerType': 'mana',
            'mask': 128,
            'id': 8,
            'name': 'Mage'
        }, {
            'powerType': 'mana',
            'mask': 16,
            'id': 5,
            'name': 'Priest'
        }, {
            'powerType': 'runic-power',
            'mask': 32,
            'id': 6,
            'name': 'Death Knight'
        }, {
            'powerType': 'mana',
            'mask': 1024,
            'id': 11,
            'name': 'Druid'
        }, {
            'powerType': 'mana',
            'mask': 256,
            'id': 9,
            'name': 'Warlock'
        }, {
            'powerType': 'energy',
            'mask': 512,
            'id': 10,
            'name': 'Monk'
        }]

        classes_.sort(key=itemgetter('id'))
        classes.sort(key=itemgetter('id'))

        self.assertEqual(classes, classes_)

        classes = self.connection.get_character_classes(battlenet.UNITED_STATES)

        for class_ in classes:
            self.assertIn(class_.power_type,
                ['mana', 'energy', 'runic-power', 'focus', 'rage'])

    def test_items(self):
        item = self.connection.get_item(battlenet.UNITED_STATES, 60249)
        # TODO

if __name__ == '__main__':
    unittest.main()
