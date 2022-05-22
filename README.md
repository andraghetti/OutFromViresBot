# OutFromViresBot

This code has been created to set up a [Telegram channel](https://t.me/+Vn9M5W852iQ2ZjA8) to alert investors of new liquidations, repay or deposits in https://vires.finance/. It is based on a scraper of https://github.com/deemru/w8io.

## Run
The code is very hacky and it needs improvement.
In the current state, two environment variables are required:

* TELEGRAM_BOT_ID: get this from [BotFather](). (E.g. `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
* TELEGRAM_CHAT_ID: get this from the [getUpdates]() function of the telegram bot. (E.g. `-1000123456789`)

You can use `export` to have them in the current shell session only:

```sh
export TELEGRAM_BOT_ID=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
export TELEGRAM_CHAT_ID=-1000123456789
python bot.py
```

If you want to run the bot in docker and forget about it:

```sh
docker run -e TELEGRAM_BOT_ID=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 -e TELEGRAM_CHAT_ID=-1000123456789 --restart unless-stopped -d andraghetti/vires-alerts
```


## Known issues

* The datetime is wrong (+1)
* useless coloredlogs dependecy since this works on docker

