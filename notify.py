import os
import math
import logging

import requests

TELEGRAM_BOT_ON = os.getenv('TELEGRAM_BOT_ON')
TELEGRAM_BOT_ON = TELEGRAM_BOT_ON.lower() == 'true' if TELEGRAM_BOT_ON is not None else False

if TELEGRAM_BOT_ON:
    BOT_ID = os.getenv('TELEGRAM_BOT_ID')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    SERVER_URL = 'https://api.telegram.org'

ALARM_CURRENCIES = ['USDC', 'USDT', 'VIRESUSDCLP']


def send(scraper, tx):
    if tx['currency'] not in ALARM_CURRENCIES or tx['amount'] < scraper.amount_threshold:
        return
    if tx is None:
        message = f'{scraper.name} bot is down.'
        silent = True
    else:
        alarm_intensity = math.floor(math.log(tx['amount']/1000, 10))
        silent = alarm_intensity < 1
        message = f"{scraper.name} {'🚨'*alarm_intensity}\n💵 *{round(tx['amount'], 3)}* %23{tx['currency']}\n⏳ _{tx['date']}_"

    if TELEGRAM_BOT_ON:
        notification = f'&disable_notification=true' if silent else ''
        url = f'{SERVER_URL}/bot{BOT_ID}/sendMessage?chat_id={CHAT_ID}&text={message}{notification}&parse_mode=Markdown'
        response = requests.get(url).json()
        if response['ok'] == False:
            logging.critical(response)
    else:
        if silent:
            logging.info(message)
        else:
            logging.critical(message)