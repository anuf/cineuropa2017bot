# -*- coding: utf-8 -*-

import PyPDF2
import re

import telebot as tb
import requests

from cineuropa2017_token import TOKEN

import gettext
import time
import datetime
import json
import os
import locale
#from cineuropa2017_utils import parsePDFprogram, load_sessions, parseFromURL
from cineuropa2017_utils2 import parsePDFprogram2, load_sessions2
import hashlib

# parseFromURL("http://www.cineuropa.gal/2016")

t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

bot = tb.TeleBot(TOKEN)

if locale.getlocale()[0] == 'es_ES':
    commands = {  # command description used in the "help" command ordered alphabetically
                  #'day n': _('Shows films from a given day'),
                  'ayuda': _('Gives you information about the available commands'),
                  'inicio': _('Get used to the bot'),
                  'hoy': _('Shows films for the current day'),
                  'mañana': _('Shows films for tomorrow'),
                  'mejores': _('Lists n top rated films'),
                  'mejores10': _('Lists top 10 rated films')
    }
elif locale.getlocale()[0] == 'gl_ES':
    commands = {  # command description used in the "help" command ordered alphabetically
                  #'day n': _('Shows films from a given day'),
                  'axuda': _('Gives you information about the available commands'),
                  'inicio': _('Get used to the bot'),
                  'hoxe': _('Shows films for the current day'),
                  'mañá': _('Shows films for tomorrow'),
                  'mellores': _('Lists n top rated films'),
                  'mellores10': _('Lists top 10 rated films')
    }
else:
    commands = {  # command description used in the "help" command ordered alphabetically
                  #'day n': _('Shows films from a given day'),
                  'help': _('Gives you information about the available commands'),
                  'start': _('Get used to the bot'),
                  'today': _('Shows films for the current day'),
                  'tomorrow': _('Shows films for tomorrow'),
                  'top': _('Lists n top rated films'),
                  'top10': _('Lists top 10 rated films')
    }

voteKeyboard = tb.types.InlineKeyboardMarkup()
voteKeyboard.add(tb.types.InlineKeyboardButton("0",callback_data = "0"),
    tb.types.InlineKeyboardButton("1",callback_data = "1"),
    tb.types.InlineKeyboardButton("2",callback_data = "2"),
    tb.types.InlineKeyboardButton("3",callback_data = "3"),
    tb.types.InlineKeyboardButton("4",callback_data = "4"),
    tb.types.InlineKeyboardButton("5",callback_data = "5"),
    tb.types.InlineKeyboardButton("6",callback_data = "6"),
    tb.types.InlineKeyboardButton("7",callback_data = "7"),
    tb.types.InlineKeyboardButton("8",callback_data = "8"),
    tb.types.InlineKeyboardButton("9",callback_data = "9"),
    tb.types.InlineKeyboardButton("10",callback_data = "10"))

markup = tb.types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = tb.types.KeyboardButton(_('/start'))
itembtn2 = tb.types.KeyboardButton(_('/help'))
itembtn3 = tb.types.KeyboardButton(_('/today'))
itembtn4 = tb.types.KeyboardButton(_('/tomorrow'))
itembtn5 = tb.types.KeyboardButton(_('/top10'))

markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

#proxy_url = "http://proxy.server:3128"
#urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    #print(call)
    print("FUNCTION: {0} : USER: {1}".format('test_callback',call.from_user.username))
    thanksMessage = _("Congratulations {0}!").format(call.from_user.first_name) \
    +". "+_("You gave a {0} to the film").format(call.data)
    bot.send_message(call.message.chat.id, thanksMessage) # send the generated help page

    # bot.edit_message_text(text="Selected option: {}".format(call.data))
# start
@bot.message_handler(commands=['start','inicio'])
def send_welcome(message):
    '''This handlert shows a welcome message.'''
    print("FUNCTION: {0} : USER: {1}".format('send_welcome',message.from_user.username))

    welcome_message = "{0} {1}. {2}".format(_("Hello"),message.from_user.first_name,_("Howdy!"))
    # Parsed PDF to JSON file
    # if not os.path.isfile("films.json"):
    #     print("NOT EXISTS")
    #     parsePDFprogram()
    # else:
    #     print("EXISTS")
    # sessions = load_sessions()
    bot.reply_to(message, welcome_message)

# help
@bot.message_handler(commands=['help','axuda','ayuda'])
def command_help(message):
    '''
    Display the commands and what are they intended for.
    '''
    print("FUNCTION: {0} : USER: {1}".format('command_help',message.from_user.username))

    chat_id = message.chat.id
    help_text = _("Available commands: \n")
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
    print("FUNCTION: {0} : USER: {1}".format('command_today',message.from_user.username))

    chat_id = message.chat.id
    day = datetime.date.today().day
    films = load_sessions2()

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
    print("FUNCTION: {0} : USER: {1}".format('command_tomorrow',message.from_user.username))

    chat_id = message.chat.id
    tomorrow = datetime.date.today()+datetime.timedelta(days=1)
    day = tomorrow.day

    films = load_sessions2()

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
    print("FUNCTION: {0} : USER: {1}".format('command_day',message.from_user.username))

    chat_id = message.chat.id

    if len(message.text.split(" ")) > 1:
        day = message.text.split(" ")[1]
        films = load_sessions2()

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
    print("FUNCTION: {0} : USER: {1}".format('command_top',message.from_user.username))

    chat_id = message.chat.id

    if len(message.text.split(" ")) > 1:
        n = message.text.split(" ")[1]
        sessions = load_sessions()
        sortedList = sorted(sessions, key = lambda x: x.rate, reverse=True)
        listaEventos = [x.toTopListHTML() for x in sortedList]
        returnMessage = "********** {0} **********\n".format(_('TOP'))
        for i in range(int(n)):
            returnMessage += "{0}".format(listaEventos[i])
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['top10','mejores10','mellores10'])
def command_top10(message):
    '''
    Show top 10 rated films.
    '''
    print("FUNCTION: {0} : USER: {1}".format('command_top10',message.from_user.username))

    chat_id = message.chat.id

    if len(message.text.split(" ")) == 1:
        sessions = load_sessions()
        sortedList = sorted(sessions, key = lambda x: x.rate, reverse=True)
        listaEventos = [x.toTopListHTML() for x in sortedList]
        returnMessage = "********** {0} **********\n".format(_('TOP 10'))
        for i in range(10):
            returnMessage += "{0}".format(listaEventos[i])
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

bot.polling()
