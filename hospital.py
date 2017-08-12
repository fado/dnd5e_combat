import json
import logging
from random import randint

from utils import roll_dice, get_bonus

log = logging.getLogger(__name__)

MONSTER_FILE = 'monsters.json'
MONSTER_OFFSET = 2  # Subtract this from len(monsters) to get upper bound of random integers generated.

class Monster(object):
    name = ""
    armour_class = 0
    hit_dice = ""
    hit_points = 0
    actions = []

    def __init__(self, name, armor_class, hit_dice, actions, constitution):
        self.name = name
        self.armour_class = armor_class
        self.hit_dice = hit_dice
        self.number_of_hit_dice = int(hit_dice.split('d')[0])
        self.actions = actions
        self.constitution = constitution
        self.hit_points = self._calculate_hit_points()

    def _calculate_hit_points(self):
        result = roll_dice(self.hit_dice) + (get_bonus(self.constitution) * self.number_of_hit_dice)
        # Make sure the HP is at least 1.
        return result if result > 1 else 1

    def get_attacks(self):
        for action in self.actions:
            if 'damage_dice' in action:
                print(action['damage_dice'])


def get_random_monster():
    monsters = get_all_monsters()

    monster = monsters[randint(0, len(monsters) - MONSTER_OFFSET)]
    log.info("".join(["Random monster selected: ", monster['name']]))

    return Monster(
        monster['name'],
        monster['armor_class'],
        monster['hit_dice'],
        monster.get('actions'),
        monster['constitution']
    )


def get_all_monsters():
    with open(MONSTER_FILE) as monster_file:
        monsters = json.load(monster_file)
    return monsters
