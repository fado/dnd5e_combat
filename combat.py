import json
import logging
from random import randint

from math import floor

MONSTER_FILE = 'monsters.json'
MONSTER_OFFSET = 2  # Subtract this from len(monsters) to get upper bound of random integers generated.

log = logging.getLogger()


class Monster(object):
    """
    Main monster class.
    """

    name = ""
    armour_class = 0
    hit_dice = ""
    hit_points = 0
    actions = []

    def __init__(self, name, armor_class, hit_dice, actions, constitution):
        self.name = name
        self.armour_class = armor_class
        self.hit_dice = hit_dice
        self.actions = actions
        self.constitution = constitution
        self.hit_points = self._calculate_hit_points()

    def _calculate_hit_points(self):
        """ Calculate the monster's hitpoints. """

        # Get the number of hit dice
        number_of_hit_dice = int(self.hit_dice.split('d')[0])
        # Get the total bonus HP to add
        bonus = number_of_hit_dice * get_bonus(self.constitution)
        # Return the total
        return int(roll_dice(self.hit_dice) + bonus)


def get_random_monster():
    """ Returns a random monster from the list. """

    with open(MONSTER_FILE) as monster_file:
        monsters = json.load(monster_file)

    monster = monsters[randint(0, len(monsters) - MONSTER_OFFSET)]
    log.info("".join(["Random monster selected: ", monster['name']]))

    return Monster(
        monster['name'],
        monster['armor_class'],
        monster['hit_dice'],
        monster['actions'],
        monster['constitution']
    )


def roll_dice(dice):
    """
    Takes a string describing the dice to be rolled and returns the total.
    """
    tokens = dice.split('d')
    dice_quantity = int(tokens[0])
    dice_type = int(tokens[1])
    total = 0

    for i in range(0, dice_quantity):
        total += randint(1, dice_type)

    return total


def get_bonus(ability_score):
    """
    Can calculate bonus for any ability score by dividing by two and rounding down.
    """
    return floor((ability_score - 10) / 2)


if __name__ == '__main__':
    # Setup the logging
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    logging.getLogger("combat").setLevel(logging.WARN)
    log.setLevel(logging.INFO)
    log.info('Starting combat...')

    monster = get_random_monster()
    log.info(monster.hit_points)
