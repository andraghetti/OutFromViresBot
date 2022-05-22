import logging
import threading
import time

import requests
from bs4 import BeautifulSoup

import notify

class Scraper(threading.Thread):
    def __init__(self, name, url, delay=15, amount_threshold=100):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
        self.txs = []
        self.killsig = False
        self.delay = delay
        self.amount_threshold = amount_threshold

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
        
        # TODO convert all the currencies to short name
        currency = 'USDC' if currency == 'USD Coin' else currency
        currency = 'VIRESUSDCLP' if currency == 'VIRES_USDC_LP' else currency

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
                    notify.send(self, tx)
            except Exception as error:
                logging.critical(f'Could not parse: {line}: {error}')

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
        notify.send(self, tx=None)
        self.shut()
        self.close()
