import logging
from math import floor
from random import randint

log = logging.getLogger(__name__)


def roll_dice(dice):
    log.info("Rolling dice: {}".format(dice))

    sets = dice.split(' + ')
    total = 0

    for set in sets:
        dice_quantity, dice_type = set.split('d')

        for i in range(0, int(dice_quantity)):
            total += randint(1, int(dice_type))

    return total


def get_bonus(ability_score):
    return floor((ability_score - 10) / 2)
