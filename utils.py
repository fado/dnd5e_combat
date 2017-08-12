from math import floor
from random import randint


def roll_dice(dice):
    tokens = dice.split('d')
    dice_quantity = int(tokens[0])
    dice_type = int(tokens[1])
    total = 0

    for i in range(0, dice_quantity):
        total += randint(1, dice_type)

    return total


def get_bonus(ability_score):
    return floor((ability_score - 10) / 2)
