import logging

from hospital import get_random_monster

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

    monster = get_random_monster()
    for attack in monster.attacks:
        log.info(attack)