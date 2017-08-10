import json
import logging
from random import randint

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

    def __init__(self, name, armor_class, hit_dice, actions):
        self.name = name
        self.armour_class = armor_class
        self.hit_dice = hit_dice
        self.actions = actions
        self.hit_points = self._calculate_hit_points()

    def _calculate_hit_points(self):
        tokens = self.hit_dice.split('d')
        dice_quantity = int(tokens[0])
        dice_type = int(tokens[1])
        total = 0

        for i in range(0, dice_quantity):
            total += randint(1, dice_type)

        return total

def get_random_monster():
    """
    Returns a random monster from the list.
    """
    with open(MONSTER_FILE) as monster_file:
        monsters = json.load(monster_file)

    monster = monsters[randint(0, len(monsters) - MONSTER_OFFSET)]
    log.info("".join(["Random monster selected: ", monster['name']]))

    return Monster(
        monster['name'],
        monster['armor_class'],
        monster['hit_dice'],
        monster['actions']
    )


if __name__ == '__main__':
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    logging.getLogger("combat").setLevel(logging.WARN)
    log.setLevel(logging.INFO)
    log.info('Starting combat...')

    monster = get_random_monster()
    log.info(monster.hit_points)
