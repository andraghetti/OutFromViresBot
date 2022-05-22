
import logging
import threading
import time

import requests
from bs4 import BeautifulSoup

import notify

class Scraper(threading.Thread):
    def __init__(self, name, url, delay=15, amount_threashold=1000):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
        self.txs = []
        self.killsig = False
        self.delay = delay
        self.amount_threashold = amount_threashold

        # Initial fetch
        lines = self.fetch_page_lines()
        for line in lines:
            tx = self.parse_line(line)
            if tx is not None and line not in self.txs:
                self.txs.append(line)

    def fetch_page_lines(self):
        html = requests.get(self.url).text
        text = BeautifulSoup(html, 'html.parser').text
        return text.split('\n')
    
    def parse_line(self, line):
        # TODO better parsing
        splitted = line.split()
        if line == '' or len(splitted) < 10:
            return None
        tx_date, tx_time, id, _, _, _, _, type, amount, currency = splitted[:10]
        if len(splitted) > 10:
            if splitted[10] != 'invoke':
                currency = f'{currency} {splitted[10]}'
        parsed = {
            'date': tx_date + ' ' + tx_time,
            'id': int(id[1:-1]),
            'type': type[:-2],
            'amount': float(amount),
            'currency': currency,
        }
        return parsed

    def check_transactions(self):
        lines = self.fetch_page_lines()
        for line in lines:
            try:
                tx = self.parse_line(line)
                if tx is not None and line not in self.txs:
                    self.txs.append(line)
                    if (tx['currency'] == 'USD Coin' or 'USDC' in tx['currency']) \
                        and tx['amount'] > self.amount_threashold:
                        logging.critical(f"NEW {tx['type'].upper()}: {tx['amount']} USDC on {tx['date']}")
                        notify.send(self.name, tx)
                    else:
                        logging.info(f"new {tx['type']}: {tx['amount']} {tx['currency']} on {tx['date']}")
                        notify.send(self.name, tx, silent=True)
            except:
                logging.debug(f'Could not parse: {line}')

    def run(self):
        while not self.killsig:
            logging.debug(f'Fetching transactions from: {self.url}')
            try:
                self.check_transactions()
                time.sleep(self.delay)
            except Exception:
                logging.exception(f'Failed to scrap: {self.url}')
    
    def cancel(self):
        logging.debug(f'Shutting: {self.name}')
        notify.send(self.name, tx=None)
        self.shut()
        self.close()
