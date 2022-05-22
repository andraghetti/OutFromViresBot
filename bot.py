
import logging
import time

import coloredlogs

from scraper import Scraper

LOADING_CHARS = "/—\|" 

TX_TYPES = [
    {
        'name': '🔄 LP Repay',
        'url': 'https://w8.io/txs/g/73309',
        'threshold': 0
    },
    {
        'name': '⬆️ Repay',
        'url': 'https://w8.io/txs/g/67801',
        'threshold': 100
    },
    {
        'name': '⬇️ Deposit',
        'url': 'https://w8.io/txs/g/64828',
        'threshold': 100
    },
]

def threads_alive(threads):
    return True in [t.is_alive() for t in threads]

def main():
    coloredlogs.install(
        fmt="%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s ",
        level=logging.INFO
    )

    threads = [
        Scraper(name=tx_t['name'], url=tx_t['url'], amount_threshold=tx_t['threshold'])
        for tx_t in TX_TYPES
    ]
    
    for thread in threads:
        thread.start()
    
    stop = False

    while threads_alive(threads):
        try:
            if not stop:
                for char in LOADING_CHARS:
                    print('Waiting for new transactions '+char, end='\r')
                    time.sleep(.2)
            [thread.join(1) for thread in threads if thread is not None and thread.is_alive()]
        except KeyboardInterrupt:
            logging.info(f'Shutting down bot...')
            stop = True
            for thread in threads:
                thread.killsig = True

if __name__ == '__main__':
    main()