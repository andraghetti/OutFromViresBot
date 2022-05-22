import os

import requests

BOT_ID = os.getenv('TELEGRAM_BOT_ID')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SERVER_URL = 'https://api.telegram.org'

def send(name, tx, silent=False):
    if tx is None:
        message = f'{name} bot is down.'
        return
    if not silent:
        message = f"🚨 💵 {name}: *{tx['amount']} {tx['currency']}* - _{tx['date']}_ 🚨"
    else:
        message = f"💵 {name}: {tx['amount']} {tx['currency']} - _{tx['date']}_"

    notification = f'&disable_notification=true' if silent else ''
    url = f'{SERVER_URL}/bot{BOT_ID}/sendMessage?chat_id={CHAT_ID}&text={message}{notification}&parse_mode=Markdown'
    requests.get(url)