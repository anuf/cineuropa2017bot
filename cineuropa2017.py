# -*- coding: utf-8 -*-

# Bot imports
import telebot as tb
import urllib3
# Project imports
from cineuropa2017_token import TOKEN
from cineuropa2017_utils import load_from_JSON

# General imports
import gettext
import requests
import re
import time
import datetime
import json
import os
import locale
import hashlib


t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

bot = tb.TeleBot(TOKEN)

def on_start(aFilename):
    try:
        print("on_start()")

        # Create a file to store sessions for push notifications if it does not
        # already exits
        if not os.path.exists(aFilename):
            # generate the file
            open(aFilename,'w')
        else:
            with open(aFilename,'r') as fname:
                d = json.load(fname)
                for k, v in d.items():
                    apologize_text = _("Hi {0}!, I'm sorry I have been out of coverage. \
Now I'm alive again! Please count on me.").format(v)
                    bot.send_message(k,apologize_text)
    except Exception as e:
        print("Error on_start(): {0}".format(e))
# Some functions taken from:
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/deep_linking.py
def extract_unique_code(message):
    # Extracts the unique_code from the sent /start command.
    return message.chat.id#text.split()[1] if len(text.split()) > 1 else None

def in_storage(unique_code):
    # Should check if a unique code exists in storage
    with open('activeSessions' ,'r') as storageFile:
        d = json.load(storageFile)
    return unique_code in d.keys()

def get_username_from_storage(unique_code):
    # Does a query to the storage, retrieving the associated username
    if os.stat("activeSessions").st_size == 0:
        return None
    else:
        with open('activeSessions','r') as storageFile:
            d = json.load(storageFile)
        return d[unique_code] if in_storage(unique_code) else None

def save_chat_id(chat_id, uname):
    # Save the chat_id->username to storage
    try:
        if os.stat("activeSessions").st_size == 0:
            d = {}
        else:
            with open('activeSessions' ,'r') as storageFile:
                d = json.load(storageFile)

        d[chat_id] = uname
        with open('activeSessions' ,'w') as storageFile:
            json.dump(d, storageFile)
    except Exception as e:
        print("ERROR save_chat_id(): {0}".format(e))

if locale.getlocale()[0] == 'es_ES':
    commands = {  # command description used in the "help" command ordered alphabetically
                  'ayuda': _('Gives you information about the available commands'),
                  'inicio': _('Get used to the bot'),
                  'hoy': _('Shows films for the current day'),
                  'mañana': _('Shows films for tomorrow'),
                  'mejores n': _('Lists n top rated films'),
                  'mejores10': _('Lists top 10 rated films'),
                  'mispuntuaciones': _('Lists your rated films')

    }
elif locale.getlocale()[0] == 'gl_ES':
    commands = {  # command description used in the "help" command ordered alphabetically
                  'axuda': _('Gives you information about the available commands'),
                  'inicio': _('Get used to the bot'),
                  'hoxe': _('Shows films for the current day'),
                  'mañá': _('Shows films for tomorrow'),
                  'mellores n': _('Lists n top rated films'),
                  'mellores10': _('Lists top 10 rated films'),
                  'asmiñaspuntuacións': _('Lists your rated films')
    }
else:
    commands = {  # command description used in the "help" command ordered alphabetically
                  'help': _('Gives you information about the available commands'),
                  'start': _('Get used to the bot'),
                  'today': _('Shows films for the current day'),
                  'tomorrow': _('Shows films for tomorrow'),
                  'top n': _('Lists n top rated films'),
                  'top10': _('Lists top 10 rated films'),
                  'myratings': _('Lists your rated films')
    }

markup = tb.types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = tb.types.KeyboardButton(_('/start'))
itembtn2 = tb.types.KeyboardButton(_('/help'))
itembtn3 = tb.types.KeyboardButton(_('/today'))
itembtn4 = tb.types.KeyboardButton(_('/tomorrow'))
itembtn5 = tb.types.KeyboardButton(_('/top10'))

markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

# proxy_url = "http://proxy.server:3128"
# urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):

    #print(call)
    print("FUNCTION: {0} : USER: {1}".format('test_callback',call.from_user.username))
    if call.data != "CANCEL":
        print(call)
        # Rating
        rate = call.data.split(":")[0]
        idFilm = call.data.split(":")[1]

        # Thanks message
        thanksMessage = _("Congratulations {0}!").format(call.from_user.first_name) \
        +". "+_("You gave a {0} to the film").format(rate)

        # Write to json file
        with open("allfilms.json", "r") as jsonFile:
            data = json.load(jsonFile)

        for d in data:
            if d["id"] == idFilm:
                print("FOUND "+ idFilm)
                # Check that teh user has not voted yet
                voters = [x[0] for x in d["rates"]]
                votes = [int(x[1]) for x in d["rates"]]
                if call.from_user.id not in voters:
                    # Update rate
                    votes.append(int(rate))
                    d["rate"] = sum(votes)/len(votes)
                    d["rates"].append([call.from_user.id, rate])
                else:
                    thanksMessage = _("Sorry, you have already rated this film!")

        with open("allfilms.json", "w") as jsonFile:
            json.dump(data, jsonFile)


        bot.send_message(call.message.chat.id, thanksMessage) # send the generated help page
    else:
        print("Callback cancelled by user.")

# start
@bot.message_handler(commands=['start','inicio'])
def send_welcome(message):
    '''This handlert shows a welcome message.'''

    #welcome_message = "{0} {1}. {2}".format(_("Hello"),message.from_user.first_name,_("Howdy!"))
    #bot.reply_to(message, welcome_message)

    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('send_welcome',chat_id))

    name_to_show = get_username_from_storage(chat_id)
    if name_to_show is None: # if the username does not exist in our database
        username = message.chat.username
        first_name = message.chat.first_name
        name_to_show = first_name
        save_chat_id(chat_id, first_name)

    reply = _("Hello {0}, how are you?").format(name_to_show)

    bot.reply_to(message, reply)

# start
@bot.message_handler(regexp='/fid_.{6}')
def filmDetail(message):
    '''This handlert shows the detailed film.'''
    print("FUNCTION: {0} : USER: {1}".format('aFilm',message.chat.id))
    chat_id = message.chat.id
    films = load_from_JSON()

    theFilm = _("No film found")
    for film in films:
        for session in film.sessions:
            if '/fid_'+session.id[:6] == message.text:
                theFilm = film.toDetail(session.date)
                thePoster = film.poster
                theFilmId = film.id
                break
    caption = _('Do you want to vote?')

    # define keyboard
    voteKeyboard = tb.types.InlineKeyboardMarkup()
    voteKeyboard.add(tb.types.InlineKeyboardButton("10",callback_data = "{0}:{1}".format(10,theFilmId)),
        tb.types.InlineKeyboardButton("9",callback_data = "{0}:{1}".format(9,theFilmId)),
        tb.types.InlineKeyboardButton("8",callback_data = "{0}:{1}".format(8,theFilmId)),
        tb.types.InlineKeyboardButton("7",callback_data = "{0}:{1}".format(7,theFilmId)),
        tb.types.InlineKeyboardButton("6",callback_data = "{0}:{1}".format(6,theFilmId)),
        tb.types.InlineKeyboardButton("5",callback_data = "{0}:{1}".format(5,theFilmId)),
        tb.types.InlineKeyboardButton("4",callback_data = "{0}:{1}".format(4,theFilmId)),
        tb.types.InlineKeyboardButton("3",callback_data = "{0}:{1}".format(3,theFilmId)),
        tb.types.InlineKeyboardButton("2",callback_data = "{0}:{1}".format(2,theFilmId)),
        tb.types.InlineKeyboardButton("1",callback_data = "{0}:{1}".format(1,theFilmId)),
        tb.types.InlineKeyboardButton("0",callback_data = "{0}:{1}".format(0,theFilmId)),
        tb.types.InlineKeyboardButton(_("Cancel"),callback_data = "CANCEL"))

    bot.reply_to(message, theFilm, parse_mode='HTML')
    bot.send_photo(chat_id, thePoster, caption = caption, reply_markup=voteKeyboard)

# help
@bot.message_handler(commands=['help','axuda','ayuda'])
def command_help(message):
    '''
    Display the commands and what are they intended for.
    '''
    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_help',chat_id))

    help_text = _('Unofficial bot for Cineuropa#31 film festival (2017).')
    help_text += '\n'+_('Film information and unofficial rating.')
    help_text += '\n'+_('No responsability on information veracity.')
    help_text += '\n'+_("Available commands:\n")

    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    #bot.send_message(chat_id, help_text,reply_markup=voteKeyboard) # send the generated help page
    bot.send_message(chat_id, help_text, reply_markup=markup)

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    print(query)

# today
@bot.message_handler(commands=['today','hoy','hoxe'])
def command_today(message):
    '''
    Show today's films.
    '''

    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_today',chat_id))
    day = datetime.date.today().day
    films = load_from_JSON()

    listaEventos = []
    for film in films:
        for y in film.sessions:
            if str(day) in y.date.split(' '):
                listaEventos.append(film.toSimple('Día {0} de novembro'.format(day)))

    if len(listaEventos) == 0:
        listaEventos = [_("No sessions today")]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# tomorrow
@bot.message_handler(commands=['tomorrow','mañana','mañá'])
def command_tomorrow(message):
    '''
    Show tomorrow's films.
    '''
    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_tomorrow',chat_id))

    tomorrow = datetime.date.today()+datetime.timedelta(days=1)
    day = tomorrow.day

    films = load_from_JSON()

    listaEventos = []
    for film in films:
        for y in film.sessions:
            if str(day) in y.date.split(' '):
                listaEventos.append(film.toSimple('Día {0} de novembro'.format(day)))

    if len(listaEventos) == 0:
        listaEventos = [_("No sessions tomorrow")]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# any day
@bot.message_handler(commands=['day','día'])
def command_day(message):

    '''
    Show films of a given day (numeric).
    '''
    chat_id = message.chat.id

    print("FUNCTION: {0} : USER: {1}".format('command_day',chat_id))

    if len(message.text.split(" ")) > 1:
        day = message.text.split(" ")[1]
        films = load_from_JSON()

        listaEventos = []
        for film in films:
            for y in film.sessions:
                if str(day) in y.date.split(' '):
                    listaEventos.append(film.toSimple('Día {0} de novembro'.format(day)))

        if len(listaEventos) == 0:
            listaEventos = [_("No sessions today")]
        for ev in listaEventos:
            bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['top','mejores','mellores'])
def command_top(message):
    '''
    Show n top rated films.
    '''
    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_top',chat_id))

    if len(message.text.split(" ")) > 1:
        n = message.text.split(" ")[1]
        if n.isdigit():
            sessions = load_from_JSON()
            sortedList = sorted(sessions, key = lambda x: x.rate, reverse=True)
            listaEventos = [x.toTopListHTML() for x in sortedList]
            returnMessage = "********** {0} **********\n".format(_('TOP'))
            for i in range(int(n)):
                returnMessage += "{0}".format(listaEventos[i])
            bot.send_message(chat_id, returnMessage, parse_mode='HTML')
        else:
            bot.send_message(chat_id, _("Invalid command"))
    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['top10','mejores10','mellores10'])
def command_top10(message):
    '''
    Show top 10 rated films.
    '''
    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_top10',chat_id))

    if len(message.text.split(" ")) == 1:
        sessions = load_from_JSON()
        sortedList = sorted(sessions, key = lambda x: x.rate, reverse=True)
        listaEventos = [x.toTopListHTML() for x in sortedList]
        returnMessage = "********** {0} **********\n".format(_('TOP 10'))
        for i in range(10):
            returnMessage += "{0}".format(listaEventos[i])
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['myratings','mispuntuaciones','asmiñaspuntuacions'])
def command_myvotes(message):
    '''Show user's ratings'''
    chat_id = message.chat.id
    print("FUNCTION: {0} : USER: {1}".format('command_myvotes',chat_id))

    if len(message.text.split(" ")) == 1:
        sessions = load_from_JSON()
        sortedList = sorted([x for x in sessions if chat_id in [y[0] for y in x.rates]], key = lambda x: x.rate, reverse=True)
        returnMessage = "********** {0} **********\n".format(_('MY RATINGS'))
        if len(sortedList) > 0:
            listaEventos = [x.toTopListHTML() for x in sortedList]
            for i in range(len(listaEventos)):
                returnMessage += "{0}".format(listaEventos[i])
        else:
                returnMessage += _("You haven't rated any film.")
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

on_start('activeSessions')

bot.polling()
