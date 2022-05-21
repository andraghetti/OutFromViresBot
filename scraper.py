
import logging
import threading
import time
import datetime

import requests
from bs4 import BeautifulSoup

class Scraper(threading.Thread):
    def __init__(self, url, delay=15):
        threading.Thread.__init__(self)
        self.url = url
        self.txs = []
        self.killsig = False
        self.delay = delay

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
        if 'repay' not in line and 'Repay' not in line:
            return None
        
        tx_date, tx_time, id, _, _, _, _, _, amount, currency = line.split()[:10]
        parsed = {
            'date': tx_date + ' ' + tx_time,
            'id': int(id[1:-1]),
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
                    if tx['currency'] == 'USD Coin' or 'USDC' in tx['currency']:
                        logging.critical(f"NEW REPAY: {tx['amount']} {tx['currency']} on {tx['date']}")
                    else:
                        logging.info(f"new repay: {tx['amount']} {tx['currency']} on {tx['date']}")
            except:
                logging.error('Could not parse: {line}')

    def run(self):
        while not self.killsig:
            logging.debug(f'Fetching transactions from: {self.url}')
            try:
                self.check_transactions()
                time.sleep(self.delay)
            except Exception:
                logging.exception(f'Failed to crawl: {self.url}')
    
    def cancel(self):
        self.shut()
        self.close()
