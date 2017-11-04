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

from cineuropa2017_utils import parsePDFprogram, load_sessions


t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

bot = tb.TeleBot(TOKEN)

commands = {  # command description used in the "help" command ordered alphabetically
              #'day n': _('Shows films from a given day'),
              'help': _('Gives you information about the available commands'),
              'start': _('Get used to the bot'),
              'today': _('Shows films for the current day'),
              'tomorrow': _('Shows films for tomorrow')
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

#proxy_url = "http://proxy.server:3128"
#urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)

@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    print(call)
    thanksMessage = _("Congratulations {0}!").format(call.from_user.first_name) \
    +". "+_("You gave a {0} to the film").format(call.data)
    bot.send_message(call.message.chat.id, thanksMessage) # send the generated help page

    # bot.edit_message_text(text="Selected option: {}".format(call.data))
# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''This handlert shows a welcome message.'''
    welcome_message = "{0} {1}. {2}".format(_("Hello"),message.from_user.first_name,_("Howdy!"))
    # Parsed PDF to JSON file
    if not os.path.isfile("films.json"):
        print("NOT EXISTS")
        parsePDFprogram()
    else:
        print("EXISTS")
    sessions = load_sessions()
    bot.reply_to(message, welcome_message)

# help
@bot.message_handler(commands=['help'])
def command_help(message):
    '''
    Display the commands and what are they intended for.
    '''
    chat_id = message.chat.id
    help_text = _("Available commands: \n")
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text,reply_markup=voteKeyboard) # send the generated help page

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    print(query)
# today
@bot.message_handler(commands=['today'])
def command_today(message):
    '''
    Show today's films.
    '''

    chat_id = message.chat.id
    day = datetime.date.today().day
    sessions = load_sessions()
    listaEventos = [x.toHTML() for x in sessions if day in x.day.split(' ')]
    if len(listaEventos) == 0:
        listaEventos = [_("No sessions today")]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# tomorrow
@bot.message_handler(commands=['tomorrow'])
def command_tomorrow(message):
    '''
    Show tomorrow's films.
    '''

    chat_id = message.chat.id
    tomorrow = datetime.date.today()+datetime.timedelta(days=1)
    day = tomorrow.day
    sessions = load_sessions()

    listaEventos = [x.toHTML() for x in sessions if day in x.day.split(' ')]
    if len(listaEventos) == 0:
        listaEventos = [_("No sessions tomorrow")]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# any day
@bot.message_handler(commands=['day'])
def command_day(message):
    '''
    Show films of a given day (numeric).
    '''

    chat_id = message.chat.id

    if len(message.text.split(" ")) > 1:
        day = message.text.split(" ")[1]
        sessions = load_sessions()
        listaEventos = [x.toHTML() for x in sessions if day in x.day.split(' ')]
        for ev in listaEventos:
            bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')
    else:
        bot.send_message(chat_id, _("Invalid command"))
bot.polling()
