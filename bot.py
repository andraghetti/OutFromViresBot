
import logging

import coloredlogs

from scraper import Scraper

LP_REPAY_URL = 'https://w8.io/txs/g/73309'
REPAY_URL = 'https://w8.io/txs/g/67801'


def threads_alive(threads):
    return True in [t.is_alive() for t in threads]

def main():
    coloredlogs.install(
        fmt="%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s ",
        level=logging.DEBUG
    )

    threads = [
        Scraper(LP_REPAY_URL),
        Scraper(REPAY_URL)
    ]
    
    for thread in threads:
        thread.start()

    while threads_alive(threads):
        try:
            [thread.join(1) for thread in threads if thread is not None and thread.is_alive()]
        except KeyboardInterrupt:
            logging.info(f'Shutting down bot...')
            for thread in threads:
                thread.killsig = True

if __name__ == '__main__':
    main()