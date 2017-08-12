import json
import logging
from random import randint

from utils import roll_dice, get_bonus

log = logging.getLogger(__name__)

MONSTER_FILE = 'monsters.json'
MONSTER_OFFSET = 2  # Subtract this from len(monsters) to get upper bound of random integers generated


class Monster:
    name = ""
    armour_class = 0
    hit_dice = ""
    hit_points = 0
    actions = []
    attacks = []

    def __init__(self, name, armor_class, hit_dice, constitution, actions):
        self.name = name
        self.armour_class = armor_class
        # Figure out hit points
        self.hit_dice = hit_dice
        self.number_of_hit_dice = int(hit_dice.split('d')[0])
        self.constitution = constitution
        self.hit_points = self._calculate_hit_points()
        # Figure out actions and attacks
        self.actions = actions
        self._get_attacks()

    def _calculate_hit_points(self):
        result = roll_dice(self.hit_dice) + (get_bonus(self.constitution) * self.number_of_hit_dice)
        # Make sure the HP is at least 1
        return result if result > 1 else 1

    def _get_attacks(self):
        for action in self.actions:
            if 'damage_dice' in action:
                self.attacks.append(action)

    def roll_attack(self, target):
        # Choose one of our attacks at random
        attack = self.attacks[randint(0, len(self.attacks) - 1)]
        log.info("Making attack: " + attack['name'])

        # Make attack roll
        natural_attack_roll = roll_dice("1d20")

        # Check for natural 1
        if natural_attack_roll == 1:
            log.info("{} rolled a natural 1!".format(self.name))

        # Check for natural 20
        elif natural_attack_roll == 20:
            log.info("{} rolled a critical hit!".format(self.name))
            self._roll_damage(attack, target, critical=True)
        else:
            attack_roll = natural_attack_roll + attack['attack_bonus']
            log.info("{} rolled {} against {}'s AC {}".format(
                self.name,
                attack_roll,
                target.name,
                target.armour_class
            ))
            if attack_roll >= target.armour_class:
                log.info("Attack hit!")
                self._roll_damage(attack, target)
            else:
                log.info("Attack missed!")

    def _roll_damage(self, attack, target, critical=False):
        if critical:
            log.info("Rolling critical damage.")
            damage = (2 * roll_dice(attack["damage_dice"])) + attack["damage_bonus"]
        else:
            log.info("Rolling normal damage.")
            damage = roll_dice(attack["damage_dice"]) + attack["damage_bonus"]

        log.info("Dealing {} damage to {}, reducing their hit points from {} to {}.".format(
            damage, target.name, target.hit_points, target.hit_points - damage
        ))

        target.hit_points -= damage


def get_random_monster():
    monsters = get_all_monsters_json()

    monster = monsters[randint(0, len(monsters) - MONSTER_OFFSET)]
    log.info("".join(["Random monster selected: ", monster['name']]))

    return Monster(
        monster['name'],
        monster['armor_class'],
        monster['hit_dice'],
        monster['constitution'],
        monster.get('actions')
    )


def get_all_monsters_json():
    with open(MONSTER_FILE) as monster_file:
        monsters = json.load(monster_file)
    return monsters
