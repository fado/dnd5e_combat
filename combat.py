import logging
from time import sleep

from hospital import get_random_monster, Monster

log = logging.getLogger()

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
            monster_a.roll_attack(monster_b)
            sleep(2)
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
