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


## JSON structure (example)
```
{
  "url" : "http://www.cineuropa.gal/peliculas/la-villa",
  "sessions" :
    [
      {
        "time" : "20:00",
        "date" : "D\u00eda 7 de novembro",
        "id" : "e05c5c879849657e2b5a60f22d950b5f",
        "place" : "TEATRO PRINCIPAL"
      }, {
        "time" : "18:15",
        "date" : "D\u00eda 12 de novembro",
        "id" : "e0f90060528746cf6a1602dd738eed61",
        "place" : "TEATRO PRINCIPAL"
      }
    ],
  "id" : "652d75b4cd784b4e61e7d460dcd5c718",
  "year" : "2017",
  "duration" : "107 min.",
  "title" : "LA VILLA",
  "poster" : "http://www.cineuropa.gal/img/posters/mini-7219324.jpg?1510068271",
  "rates" : [],
  "rate" : 0,
  "director" : "\u2013 Robert Gu\u00e9diguian",
  "synopsis": "Nunha pequena ba\\xc3\\xada preto de Marsella at\\xc3\\xb3pase unha pintoresca vila propiedade dun anci\\xc3\\xa1n. Os seus tres fillos re\\xc3\\xbanense con el para acompa\\xc3\\xb1alo nos seus \\xc3\\xbaltimos d\\xc3\\xadas. \\xc3\\x89 hora de que sopesen o que herdaron dos ideais do seu pai e do esp\\xc3\\xadrito de comunidade que el creou neste lugar m\\xc3\\xa1xico. A chegada dunha patera a unha enseada pr\\xc3\\xb3xima converter\\xc3\\xa1 a reflexi\\xc3\\xb3n en axitaci\\xc3\\xb3n."
}
```
## Useful links:
* [How to use gettext](https://pymotw.com/3/gettext/)
* [Translating with gettext](https://www.icanlocalize.com/site/tutorials/how-to-translate-with-gettext-po-and-pot-files/)
* [Poedit](https://poedit.net/)
