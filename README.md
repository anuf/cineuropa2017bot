# Telegram Bot for Cineuropa 2017 films
Films from Cineuropa 2017 film festival parsed from official PDF program to be accesed through this Telegram Bot.

It is written in Python based on **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)**. There are other wrappers for the Telegram API, but we have tried this for the moment.

## Prerequisites

You have obtain an API token with [@BotFather](https://core.telegram.org/bots#botfather). Copy or rename __cineuropa2017_token_py.tmpl__ template file to file __cineuropa2017_token_py__ and place the TOKEN on it.

## How to run the bot.

On a server running Python execute:

    python cineuropa2017.py

## Available commands

* __/start__ Sends you a welcome message.
* __/help__ Displays available commands.
* __/today__ Shows today's films.
* __/tomorrow__ Shows tomorrow's films
* __/day n__ Shows events for day n

## Test it!
There's a Telegram bot called **Cineuropa2017Bot** that's online. You can find it searching through your telegram account.

## Useful links:
* [How to use gettext](https://pymotw.com/3/gettext/)
* [Translating with gettext](https://www.icanlocalize.com/site/tutorials/how-to-translate-with-gettext-po-and-pot-files/)
* [Poedit](https://poedit.net/)
