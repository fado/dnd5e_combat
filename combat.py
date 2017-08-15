import logging
from random import randint, choice

from time import sleep

from hospital import get_random_monster
from utils import roll_dice

log = logging.getLogger()


def roll_attack(attacker, attack, target):
    log.info("Making attack: " + attack['name'])

    # Make attack roll
    natural_attack_roll = roll_dice("1d20")

    # Check for natural 1
    if natural_attack_roll == 1:
        log.info("{} rolled a natural 1!".format(attacker.name))

    # Check for natural 20
    elif natural_attack_roll == 20:
        log.info("{} rolled a critical hit!".format(attacker.name))
        roll_damage(attack, target, critical=True)
    else:
        attack_roll = natural_attack_roll + attack['attack_bonus']
        log.info("{} rolled {} against {}'s AC {}".format(
            attacker.name,
            attack_roll,
            target.name,
            target.armour_class
        ))
        if attack_roll >= target.armour_class:
            log.info("Attack hit!")
            roll_damage(attack, target)
        else:
            log.info("Attack missed!")


def roll_damage(attack, target, critical=False):
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

if __name__ == '__main__':
    # Setup the logging
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    logging.getLogger("combat").setLevel(logging.WARN)
    log.setLevel(logging.INFO)
    log.info('Starting combat...')

    monster_a = get_random_monster()
    monster_b = get_random_monster()

    try:
        while monster_b.hit_points > 0:
            attack = choice(monster_a.attacks)
            roll_attack(monster_a, attack, monster_b)
            #sleep(2)
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
