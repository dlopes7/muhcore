import operator
import collections
import datetime
from .enums import RACE, CLASS, QUALITY, RACE_TO_FACTION, RAIDS, EXPANSION
from .utils import make_icon_url, normalize, make_connection

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['Character', 'Guild', 'Realm', 'Raid']


class Thing(object):
    def __init__(self, data):
        self._data = data

    def to_json(self):
        return json.dumps(self._data)

    def __repr__(self):
        return '<%s>' % (self.__class__.__name__,)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return getattr(self, '_data') == getattr(other, '_data')

    def __ne__(self, other):
        return not self.__eq__(other)


class LazyThing(Thing):
    def __init__(self, data, fields=None):
        super(LazyThing, self).__init__(data)

        self._fields = set(fields or [])

    def _refresh_if_not_present(self, field):
        if not hasattr(self, '_' + field):
            if field not in self._data:
                self.refresh(field)

            return True

    def _delete_property_fields(self):
        for field in self._fields:
            try:
                delattr(self, '_' + field)
            except AttributeError:
                pass

    def _populate_data(self, data):
        raise NotImplementedError

    def refresh(self, *fields):
        raise NotImplementedError


class Character(LazyThing):
    MALE = 0
    FEMALE = 1

    ALLIANCE = 'Alliance'
    HORDE = 'Horde'

    DRAENEI = 'Draenei'
    DWARF = 'Dwarf'
    GNOME = 'Gnome'
    HUMAN = 'Human'
    NIGHT_ELF = 'Night Elf'
    WORGEN = 'Worgen'

    BLOOD_ELF = 'Blood Elf'
    UNDEAD = 'Undead'
    GOBLIN = 'Goblin'
    ORC = 'Orc'
    TAUREN = 'Tauren'
    TROLL = 'Troll'

    DEATH_KNIGHT = 'Death Knight'
    DRUID = 'Druid'
    HUNTER = 'Hunter'
    MAGE = 'Mage'
    PALADIN = 'Paladin'
    PRIEST = 'Priest'
    ROGUE = 'Rogue'
    SHAMAN = 'Shaman'
    WARLOCK = 'Warlock'
    WARRIOR = 'Warrior'

    ALCHEMY = 'Alchemy'
    BLACKSMITHING = 'Blacksmithing'
    ENCHANTING = 'Enchanting'
    ENGINEERING = 'Engineering'
    HERBALISM = 'Herbalism'
    INSCRIPTION = 'Inscription'
    JEWELCRATING = 'Jewelcrafting'
    LEATHERWORKING = 'Leatherworking'
    MINING = 'Mining'
    Skinning = 'Skinning'
    TAILORING = 'Tailoring'

    ARCHAEOLOGY = 'Archaeology'
    COOKING = 'Cooking'
    FIRST_AID = 'First Aid'
    FISHING = 'Fishing'

    STATS = 'stats'
    TALENTS = 'talents'
    ITEMS = 'items'
    REPUTATIONS = 'reputation'
    TITLES = 'titles'
    PROFESSIONS = 'professions'
    APPEARANCE = 'appearance'
    COMPANIONS = 'companions'
    MOUNTS = 'mounts'
    GUILD = 'guild'
    QUESTS = 'quests'
    HUNTER_PETS = 'hunterPets'
    PROGRESSION = 'progression'
    ACHIEVEMENTS = 'achievements'
    ALL_FIELDS = [STATS, TALENTS, ITEMS, REPUTATIONS, TITLES, PROFESSIONS,
                  APPEARANCE, COMPANIONS, MOUNTS, GUILD, QUESTS, HUNTER_PETS,
                  PROGRESSION, ACHIEVEMENTS]

    def __init__(self, region, realm=None, name=None, data=None, fields=None, connection=None):
        super(Character, self).__init__(data, fields)

        self.region = region
        self.connection = connection or make_connection()

        if realm and name and not data:
            data = self.connection.get_character(region, realm, name, raw=True, fields=self._fields)

        self._populate_data(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s@%s>' % (self.__class__.__name__, self.name, normalize(self._data['realm']))

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False

        return self.connection == other.connection \
            and self.name == other.name \
            and self.get_realm_name() == other.get_realm_name()

    def _populate_data(self, data):
        self._data = data
        #print(data)

        self.name = normalize(data['name'])
        self.level = data['level']
        self.class_ = data['class']
        self.race = data['race']
        self.thumbnail = data['thumbnail']
        self.gender = data['gender']
        self.achievement_points = data['achievementPoints']
        self.faction = RACE_TO_FACTION.get(self.race, 'unknown')

        if Character.GUILD in self._fields and Character.GUILD not in self._data:
            self._data[Character.GUILD] = None

        if 'lastModified' in data:
            self.last_modified = datetime.datetime.fromtimestamp(data['lastModified'] / 1000)
        else:
            self.last_modified = None

        if 'hunterPets' in data:
            self.hunter_pets = [HunterPet(hunter_pet) for hunter_pet in self._data['hunterPets']]

    @property
    def realm(self):
        if not hasattr(self, '_realm'):
            self._realm = Realm(self.region, self._data['realm'], connection=self.connection)

        return self._realm

    @property
    def professions(self):
        if self._refresh_if_not_present(Character.PROFESSIONS):
            professions = {
                'primary': [],
                'secondary': []
            }

            for type_ in list(professions.keys()):
                professions[type_] = [Profession(self, profession)
                    for profession in self._data[Character.PROFESSIONS][type_]]

            self._professions = professions

        return self._professions

    @property
    def progression(self):
        if self._refresh_if_not_present(Character.PROGRESSION):
            instances = { 'raids': [] }
            for type_ in list(instances.keys()):
                instances[type_] = [Instance(self, instance, type_) for instance in self._data[Character.PROGRESSION][type_]]
            self._progression = instances

        return self._progression

    @property
    def equipment(self):
        if self._refresh_if_not_present(Character.ITEMS):
            self._items = Equipment(self, self._data[Character.ITEMS])

        return self._items

    @property
    def mounts(self):
        if self._refresh_if_not_present(Character.MOUNTS):
            self._mounts = list(self._data[Character.MOUNTS])

        return self._mounts

    @property
    def companions(self):
        if self._refresh_if_not_present(Character.COMPANIONS):
            self._companions = list(self._data[Character.COMPANIONS])

        return self._companions

    @property
    def reputations(self):
        if self._refresh_if_not_present(Character.REPUTATIONS):
            self._reputation = [Reputation(reputation) for reputation in self._data[Character.REPUTATIONS]]

        return self._reputation

    @property
    def titles(self):
        if self._refresh_if_not_present(Character.TITLES):
            self._titles = [Title(self, title) for title in self._data[Character.TITLES]]

        return self._titles

    @property
    def guild(self):
        if self._refresh_if_not_present(Character.GUILD):
            data = self._data[Character.GUILD]

            if data:
                data['side'] = self.faction.lower()

                self._guild = Guild(self.region, realm=self._data['realm'], data=data, connection=self.connection)
            else:
                self._guild = None

        return self._guild

    @property
    def appearance(self):
        if self._refresh_if_not_present(Character.APPEARANCE):
            self._appearance = Appearance(self._data[Character.APPEARANCE])

        return self._appearance

    @property
    def talents(self):
        if self._refresh_if_not_present(Character.TALENTS):
            self._talents = [Build(self, build) for build in self._data[Character.TALENTS]]

        return self._talents

    @property
    def stats(self):
        if self._refresh_if_not_present(Character.STATS):
            self._stats = Stats(self, self._data[Character.STATS])

        return self._stats

    @property
    def achievements(self):
        if self._refresh_if_not_present(Character.ACHIEVEMENTS):
            self._achievements = {}

            achievements_completed = self._data['achievements']['achievementsCompleted']
            achievements_completed_ts = self._data['achievements']['achievementsCompletedTimestamp']

            for id_, timestamp in zip(achievements_completed, achievements_completed_ts):
                self._achievements[id_] = datetime.datetime.fromtimestamp(timestamp / 1000)

        return self._achievements

    def refresh(self, *fields):
        for field in fields:
            self._fields.add(field)

        self._populate_data(self.connection.get_character(self.region, self._data['realm'],
            self.name, raw=True, fields=self._fields))

        self._delete_property_fields()

    def get_realm_name(self):
        return normalize(self._data['realm'])

    def get_class_name(self):
        return CLASS.get(self.class_, 'Unknown')

    def get_spec_name(self):
        for talent in self.talents:
            if talent.selected:
                return talent.name

        return ''

    def get_full_class_name(self):
        spec_name = self.get_spec_name()
        class_name = self.get_class_name()

    def get_spec_icon(self):
        for talent in self.talents:
            if talent.selected:
                return talent.get_icon_url()

        return ''

        return ('%s %s' % (spec_name, class_name)).strip()

    def get_race_name(self):
        return RACE.get(self.race, 'Unknown')

    def get_thumbnail_url(self):
        return 'http://%(region)s.battle.net/static-render/%(region)s/%(path)s' % {
            'region': self.region,
            'path': self.thumbnail
        }


class Title(Thing):
    def __init__(self, character, data):
        super(Title, self).__init__(data)

        self._character = character
        self.id = data['id']
        self.format = data['name']
        self.selected = data.get('selected', False)

    def __str__(self):
        return self.format % self._character.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.format)


class Reputation(Thing):
    def __init__(self, data):
        super(Reputation, self).__init__(data)

        self.id = data['id']
        self.name = data['name']
        self.standing = data['standing']
        self.value = data['value']
        self.max = data['max']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    @property
    def percent(self):
        return int(100.0 * self.value / self.max)


class Stats(Thing):
    def __init__(self, character, data):
        super(Stats, self).__init__(data)

        self._character = character

        self.agility = data['agi']
        self.armor = data['armor']
        self.attack_power = data['attackPower']
        self.block = data['block']
        self.block_rating = data['blockRating']
        self.crit = data['crit']
        self.crit_rating = data['critRating']
        self.dodge = data['dodge']
        self.dodge_rating = data['dodgeRating']
        self.expertise_rating = data['expertiseRating']
        self.haste_rating = data['hasteRating']
        self.health = data['health']
        self.hit_rating = data['hitRating']
        self.intellect = data['int']
        self.main_hand_damage_max = data['mainHandDmgMax']
        self.main_hand_damage_min = data['mainHandDmgMin']
        self.main_hand_dps = data['mainHandDps']
        self.main_hand_expertise = data['mainHandExpertise']
        self.main_hand_speed = data['mainHandSpeed']
        self.mana_regen = data['mana5']
        self.mana_regen_combat = data['mana5Combat']
        self.mastery = data['mastery']
        self.mastery_rating = data['masteryRating']
        self.off_hand_damage_max = data['offHandDmgMax']
        self.off_hand_damage_min = data['offHandDmgMin']
        self.off_hand_dps = data['offHandDps']
        self.off_hand_expertise = data['offHandExpertise']
        self.off_hand_speed = data['offHandSpeed']
        self.parry = data['parry']
        self.parry_rating = data['parryRating']
        self.power = data['power']
        self.power_type = data['powerType']
        self.ranged_attack_power = data['rangedAttackPower']
        self.ranged_crit = data['rangedCrit']
        self.ranged_crit_rating = data['rangedCritRating']
        self.ranged_damage_max = data['rangedDmgMax']
        self.ranged_damage_min = data['rangedDmgMin']
        self.ranged_dps = data['rangedDps']
        self.ranged_hit_rating = data['rangedHitRating']
        self.ranged_speed = data['rangedSpeed']
        self.resilience = data['pvpResilience']
        self.resilience_rating = data['pvpResilienceRating']
        self.spell_crit = data['spellCrit']
        self.spell_crit_rating = data['spellCritRating']
        self.spell_penetration = data['spellPen']
        self.spell_power = data['spellPower']
        self.spirit = data['spr']
        self.stamina = data['sta']
        self.strength = data['str']

    @property
    def hit(self):
        return self._convert_rating_to_percent({
            60: 9.37931,
            70: 14.7905,
            80: 40.7548,
            85: 120.109
        }, self.hit_rating)

    @property
    def spell_hit(self):
        return self._convert_rating_to_percent({
            60: 8,
            70: 12.6154,
            80: 26.232,
            85: 102.446
        }, self.hit_rating)

    @property
    def haste(self):
        return self._convert_rating_to_percent({
            60: 10,
            70: 15.77,
            80: 32.79,
            85: 128.05701
        }, self.haste_rating)

    def _convert_rating_to_percent(self, ratios, rating):
        percent = None

        for threshold in sorted(ratios.keys()):
            if self._character.level <= threshold:
                percent = rating / ratios[threshold]

        if percent is None:
            percent = rating / rating[max(ratios.keys())]

        return percent


class Appearance(Thing):
    def __init__(self, data):
        super(Appearance, self).__init__(data)

        self.face = data['faceVariation']
        self.feature = data['featureVariation']
        self.hair = data['hairVariation']
        self.hair_color = data['hairColor']
        self.show_cloak = data['showCloak']
        self.show_helm = data['showHelm']
        self.skin_color = data['skinColor']


class Equipment(Thing):
    def __init__(self, character, data):
        super(Equipment, self).__init__(data)

        self._character = character
        self.connection = character.connection

        self.average_item_level = data['averageItemLevel']
        self.average_item_level_equipped = data['averageItemLevelEquipped']

        print ('mainhand', data.get('mainhand'))
        print ('offhand', data.get('offhand'))
        print ('onehand', data.get('onehand'))

        self.main_hand = EquippedItem(self._character.region, data['mainHand'], self._character.connection, slot='Main Hand') if data.get('mainHand') else None
        self.off_hand = EquippedItem(self._character.region, data['offHand'], self._character.connection, slot='Held In Off-hand' ) if data.get('offHand') else None
        self.ranged = EquippedItem(self._character.region, data['ranged'], self._character.connection, slot='Ranged Right') if data.get('ranged') else None

        self.head = EquippedItem(self._character.region, data['head'], self._character.connection, slot='Head') if data.get('head') else None
        self.neck = EquippedItem(self._character.region, data['neck'], self._character.connection, slot='Neck') if data.get('neck') else None
        self.shoulder = EquippedItem(self._character.region, data['shoulder'], self._character.connection, slot='Shoulder') if data.get('shoulder') else None
        self.back = EquippedItem(self._character.region, data['back'], self._character.connection, slot='Back') if data.get('back') else None
        self.chest = EquippedItem(self._character.region, data['chest'], self._character.connection, slot='Chest') if data.get('chest') else None
        self.shirt = EquippedItem(self._character.region, data['shirt'], self._character.connection, slot='Shirt') if data.get('shirt') else None
        self.tabard = EquippedItem(self._character.region, data['tabard'], self._character.connection, slot='Tabard') if data.get('tabard') else None
        self.wrist = EquippedItem(self._character.region, data['wrist'], self._character.connection, slot='Wrist') if data.get('wrist') else None

        self.hands = EquippedItem(self._character.region, data['hands'], self._character.connection, slot='Hands') if data.get('hands') else None
        self.waist = EquippedItem(self._character.region, data['waist'], self._character.connection , slot='Waist') if data.get('waist') else None
        self.legs = EquippedItem(self._character.region, data['legs'], self._character.connection, slot='Legs') if data.get('legs') else None
        self.feet = EquippedItem(self._character.region, data['feet'], self._character.connection, slot='Feet') if data.get('feet') else None
        self.finger1 = EquippedItem(self._character.region, data['finger1'], self._character.connection, slot='Finger') if data.get('finger1') else None
        self.finger2 = EquippedItem(self._character.region, data['finger2'], self._character.connection, slot='Finger') if data.get('finger2') else None
        self.trinket1 = EquippedItem(self._character.region, data['trinket1'], self._character.connection, slot='Trinket') if data.get('trinket1') else None
        self.trinket2 = EquippedItem(self._character.region, data['trinket2'], self._character.connection, slot='Trinket') if data.get('trinket2') else None

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise IndexError


class Build(Thing):
    def __init__(self, character, data):
        super(Build, self).__init__(data)

        self._character = character

        spec = data.get('spec', {})

        if 'spec' in data:
            self.icon = spec.get('icon')
            self.name = spec.get('name')
        else:
            self.icon = 'inv_misc_questionmark'
            self.name = 'None'

        self.talents = data['talents']
        self.selected = data.get('selected', False)
        self.glyphs = {
            'prime': [],
            'major': [],
            'minor': [],
        }
        self.trees = []

    def __str__(self):
        return self.name + ' (%d/%d/%d)' % tuple(map(operator.attrgetter('total'), self.trees))

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def get_icon_url(self, size='large'):
        return make_icon_url(self._character.region, self.icon, size)


class Glyph(Thing):
    def __init__(self, character, data):
        super(Glyph, self).__init__(data)

        self._character = character

        self.name = data['name']
        self.glyph = data['glyph']
        self.item = data['item']
        self.icon = data['icon']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    def get_icon_url(self, size='large'):
        return make_icon_url(self._character.region, self.icon, size)


class Instance(Thing):
    def __init__(self, character, data, type_):
        super(Instance, self).__init__(data)

        self._character = character
        self._type = type_

        self.name = data['name']
        self.normal = data['normal']
        self.heroic = data['heroic']
        self.id = data['id']

        self.bosses = [Boss(self, boss) for boss in data['bosses']]

    def is_complete(self, type_):
        assert type_ in ['normal', 'heroic']
        return self._data[type_] == 2

    def is_started(self, type_):
        assert type_ in ['normal', 'heroic']
        return self._data[type_] == 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class Boss(Thing):
    def __init__(self, instance, data):
        super(Boss, self).__init__(data)

        self._instance = instance

        self.id = data['id']
        self.name = data['name']
        self.normal = data.get('normalKills', 0)
        self.heroic = data.get('heroicKills', 0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class Profession(Thing):
    def __init__(self, character, data):
        super(Profession, self).__init__(data)

        self._character = character

        self.id = data['id']
        self.name = data['name']
        self.max = data['max']
        self.rank = data['rank']
        self.icon = data['icon']
        self.recipes = data['recipes']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class HunterPet(Thing):
    def __init__(self, data):
        super(HunterPet, self).__init__(data)

        self.name = data['name']
        self.creature = data['creature']
        self.slot = data['slot']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class Guild(LazyThing):
    ACHIEVEMENTS = 'achievements'
    MEMBERS = 'members'
    ALL_FIELDS = [ACHIEVEMENTS, MEMBERS]

    def __init__(self, region, realm=None, name=None, data=None, fields=None, connection=None):
        super(Guild, self).__init__(data, fields)

        self.region = region
        self.connection = connection or make_connection()

        if realm and name:
            data = self.connection.get_guild(region, realm, name, raw=True, fields=self._fields)
            data['realm'] = realm  # Copy over realm since API does not provide it!

        self._populate_data(data)

    def __len__(self):
        if 'members' in self._data and isinstance(self._data['members'], int):
            return self._data['members']

        return len(self.members)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s@%s>' % (self.__class__.__name__, self.name, self._data['realm'])

    def _populate_data(self, data):
        if self._data is not None:
            data['realm'] = self._data['realm']  # Copy over realm since API does not provide it!

        self._data = data
       # print (data['name'])
       # print (normalize(data['name']))

        self.name = normalize(data['name'])
        self.emblem = Emblem(data['emblem']) if 'emblem' in data else None
        self.achievement_points = data['achievementPoints']
        self.faction = ({
            0: 'alliance',
            1: 'horde',
        }[data['side']] if isinstance(data['side'], int) else data['side']).capitalize()

    def refresh(self, *fields):
        for field in fields:
            self._fields.add(field)

        self._populate_data(self.connection.get_guild(self.region, self._data['realm'],
            self.name, raw=True, fields=self._fields))

        self._delete_property_fields()

    @property
    def perks(self):
        return [perk for perk in self.connection.get_guild_perks(self.region) if perk.guild_level <= self.level]

    @property
    def rewards(self):
        return [reward for reward in self.connection.get_guild_rewards(self.region)
                if reward.min_guild_level <= self.level]

    @property
    def achievements(self):
        if self._refresh_if_not_present(Guild.ACHIEVEMENTS):
            self._achievements = {}

            achievements_completed = self._data['achievements']['achievementsCompleted']
            achievements_completed_ts = self._data['achievements']['achievementsCompletedTimestamp']

            for id_, timestamp in zip(achievements_completed, achievements_completed_ts):
                self._achievements[id_] = datetime.datetime.fromtimestamp(timestamp / 1000)

#            criteria = self._data['achievements']['criteria']
#            criteria_quantity = self._data['achievements']['criteriaQuantity']
#            criteria_created = self._data['achievements']['criteriaCreated']
#            criteria_ts = self._data['achievements']['criteriaTimestamp']
#
#            for id_, quantity, created, timestamp in zip(criteria, criteria_quantity, criteria_created, criteria_ts):
#                pass

        return self._achievements

    @property
    def members(self):
        if self._refresh_if_not_present(Guild.MEMBERS):
            self._members = []

            for member in self._data[Guild.MEMBERS]:
                character = Character(self.region, data=member['character'], connection=self.connection, fields=[Character.ITEMS])

                if not character.name:
                    continue

                character._guild = self

                self._members.append({
                    'character': character,
                    'rank': member['rank']
                })

        return self._members

    @property
    def realm(self):
        if not hasattr(self, '_realm'):
            self._realm = Realm(self.region, self._data['realm'], connection=self.connection)

        return self._realm

    def get_leader(self):
        for member in self.members:
            if member['rank'] is 0:
                return member['character']

    def get_realm_name(self):
        return normalize(self._data['realm'])


class Emblem(Thing):
    def __init__(self, data):
        super(Emblem, self).__init__(data)

        self.border = data['border']
        self.border_color = data['borderColor']
        self.icon = data['icon']
        self.icon_color = data['iconColor']
        self.background_color = data['backgroundColor']


class Perk(Thing):
    def __init__(self, region, data):
        super(Perk, self).__init__(data)

        self._region = region

        self.id = data['spell']['id']
        self.name = data['spell']['name']
        self.description = data['spell']['description']
        self.subtext = data['spell'].get('subtext', '')
        self.cooldown = data['spell'].get('cooldown', '')
        self.cast_time = data['spell'].get('castTime')
        self.icon = data['spell'].get('icon')
        self.range = data['spell'].get('range')
        self.guild_level = data['guildLevel']

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.subtext:
            return '<%s: %s [%s]>' % (self.__class__.__name__, self.name, self.subtext)

        return '<%s: %s>' % (self.__class__.__name__, self.name)

    def get_icon_url(self, size='large'):
        if not self.icon:
            return ''

        return make_icon_url(self._region, self.icon, size)


class Reward(Thing):
    def __init__(self, region, data):
        super(Reward, self).__init__(data)

        self.min_guild_level = data['minGuildLevel']
        self.min_guild_reputation = data['minGuildRepLevel']
        self.races = data.get('races', [])
        self.achievement = data.get('achievement')
        self.item = EquippedItem(region, data['item'])

    def __str__(self):
        return self.item.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def get_race_names(self):
        return [RACE[race] for race in self.races]


class Realm(Thing):
    PVP = 'pvp'
    PVE = 'pve'
    RP = 'rp'
    RPPVP = 'rppvp'

    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

    def __init__(self, region, name=None, data=None, connection=None):
        super(Realm, self).__init__(data)

        self.region = region
        self.connection = connection or make_connection()

        if name and not data:
            data = self.connection.get_realm(region, name, raw=True)

        self._populate_data(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s(%s)>' % (self.__class__.__name__, self.name, self.region.upper())

    def _populate_data(self, data):
        self._data = data

        self.name = normalize(data['name'])
        self.slug = data['slug']
        self.status = data['status']
        self.queue = data['queue']
        self.population = data['population']
        self.type = data['type']

    def refresh(self):
        self._populate_data(self.connection.get_realm(self.name, raw=True))

    def has_queue(self):
        return self.queue

    def is_online(self):
        return self.status

    def is_offline(self):
        return not self.status


class EquippedItem(Thing):
    def __init__(self, region, data, connection=None, slot=None):
        super(EquippedItem, self).__init__(data)

        slots = {0: 'None',1: 'Head',2: 'Neck',3: 'Shoulder',4: 'Shirt',5: 'Chest',
                 6: 'Waist',7: 'Legs',8: 'Feet',9: 'Wrist',10: 'Hands',11: 'Finger',
                 12: 'Trinket',13: 'One-Hand',14: 'Shield',15: 'Ranged',16: 'Cloak',
                 17: 'Two-Hand',18: 'Bag',19: 'Tabard',20: 'Robe',21: 'Main Hand',
                 22: 'Off Hand',23: 'Held In Off-hand',24: 'Ammo',25: 'Thrown',
                 26: 'Ranged Right',28: 'Relic'}

        self._region = region


        self.id = data['id']
        self.name = data['name']
        self.quality = data['quality']
        self.icon = data['icon']

        self.ilvl = data['itemLevel'] #Adicionado por David Lopes
        self.bonus = data['bonusLists'] #Adicionado por David Lopes
        self.context = data['context'] #Adicionado por David Lopes

        #The next part is needed because the Character.ITEMS that comes with the Guild API 
        #does not return full item description, we need the slot info.
        try:
            self.slot = slots[data['inventoryType']]
        except KeyError:
            print ('data[\'inventoryType\']','not included')
            #print ('inventoryType not found, this comes from a Guild query')
            #full_item = self.connection.get_item(region, self.id)
            self.slot = slot
        

        #self.reforge = data['tooltipParams'].get('reforge')
        #self.set = data['tooltipParams'].get('set')
        #self.enchant = data['tooltipParams'].get('enchant')
        #self.extra_socket = data['tooltipParams'].get('extraSocket', False)

        #self.gems = collections.defaultdict(lambda: None)

        #for key, value in list(data['tooltipParams'].items()):
        #    if key.startswith('gem'):
        #        self.gems[int(key[3:])] = value

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

    def get_quality_name(self):
        return QUALITY.get(self.quality, 'Unknown')

    def get_icon_url(self, size='large'):
        return make_icon_url(self._region, self.icon, size)


class Class(Thing):
    def __init__(self, data):
        super(Class, self).__init__(data)

        self.id = data['id']
        self.mask = data['mask']
        self.name = data['name']
        self.power_type = data['powerType']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

class Race(Thing):
    def __init__(self, data):
        super(Race, self).__init__(data)

        self.id = data['id']
        self.mask = data['mask']
        self.name = data['name']
        self.side = data['side']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)

class Raid(Thing):
    def __init__(self, id):
        self.id = id

    def expansion(self):
        for exp, ids in list(RAIDS.items()):
            if self.id in ids:
                for e in list(EXPANSION.keys()):
                    if EXPANSION[e][0] == exp:
                        return exp, EXPANSION[e][1]
        return (None, None)
