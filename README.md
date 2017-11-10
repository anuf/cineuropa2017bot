# Telegram Bot for Cineuropa 2017 films
Films from Cineuropa 2017 film festival parsed from official site to be accessed
through this Telegram Bot.

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


## JSON structure (example)
```
{
    "id": "652d75b4cd784b4e61e7d460dcd5c718",
    "year": "2017",
    "synopsis": "Nunha pequena ba\u00eda preto de Marsella at\u00f3pase unha pintoresca vila propiedade dun anci\u00e1n. Os seus tres fillos re\u00fanense con el para acompa\u00f1alo nos seus \u00faltimos d\u00edas. \u00c9 hora de que sopesen o que herdaron dos ideais do seu pai e do esp\u00edrito de comunidade que el creou neste lugar m\u00e1xico. A chegada dunha patera a unha enseada pr\u00f3xima converter\u00e1 a reflexi\u00f3n en axitaci\u00f3n.",
    "director": "Robert Gu\u00e9diguian",
    "rates": [],
    "duration": "107 min.",
    "gender": "Ficci\u00f3n",
    "sessions": [
        {
            "id": "e05c5c879849657e2b5a60f22d950b5f",
            "time": "20:00",
            "date": "D\u00eda 7 de novembro",
            "place": "TEATRO PRINCIPAL"
        },
        {
            "id": "e0f90060528746cf6a1602dd738eed61",
            "time": "18:15",
            "date": "D\u00eda 12 de novembro",
            "place": "TEATRO PRINCIPAL"
        }
    ],
    "countries": "Francia",
    "url": "http://www.cineuropa.gal/peliculas/la-villa",
    "poster": "http://www.cineuropa.gal/img/posters/mini-7219324.jpg?1510068271",
    "rate": 0,
    "title": "LA VILLA"
}
```
## Useful links:
* [How to use gettext](https://pymotw.com/3/gettext/)
* [Translating with gettext](https://www.icanlocalize.com/site/tutorials/how-to-translate-with-gettext-po-and-pot-files/)
* [Poedit](https://poedit.net/)
