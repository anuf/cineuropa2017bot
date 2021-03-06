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
import logging

t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

bot = tb.TeleBot(TOKEN)

#if not os.path.exists('cineuropa2017.log'):
endtime = datetime.datetime(2017,11,29,0,0,0,0)

def on_start(aFilename):
    try:
        print("on_start()")

        logging.basicConfig(filename='cineuropa2017.log',level=logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s')

        logging.info("Started")
        # Create a file to store sessions for push notifications if it does not
        # already exits
        if not os.path.exists(aFilename):
            # generate the file
            open(aFilename,'w')
        else:
            with open(aFilename,'r') as fname:
                d = json.load(fname)
                for k, v in d.items():
                    apologize_text = _("Hi {0}!, I'm sorry I have been out of \
coverage for a while. Possibly updating something. Anyway, now I'm alive again! \
Please count on me.").format(v)
                    update_text = _("Hi {0}!, Now you can try the Cineuropa2017Bot inline!!! \
Write <b>@Cineuropa2017Bot</b> at the beginning of a message in any chat! \
You will see a list of today's next films. Choose one to send detailed info about the film to the chat \
or touch the image to navigate to Cineuropa site detailed info. Have fun!").format(v)
                    notification_text = _("Hi {0}!, Cineuropa 2017 film festival is ending soon. \
Thanks for participating in this experiment. We hope to be back next year with more features. \
Hurry up to rate your latest films and of course... have fun!").format(v)

                    if datetime.datetime.today() > endtime:
                        bot.send_message(k, _("<b>Hi {0}!</b>\nCineuropa 2017 film festival is over. \
Thanks for participating in this experiment. We hope to be back next year with more features. \
Rating has been already disabled but you can still interact for some days with the bot with simple commands like /myrates, /mystats or /top10.\n \
Comments and suggestions are all welcome in utopica.ml@gmail.com.\n<b>Please stay tuned for upcomming updates.</b>"
).format(v), parse_mode='html')
                    else:
                        #bot.send_message(k,apologize_text)
                        #bot.send_message(k,notification_text, parse_mode='HTML')
                        print('pass')
                        pass
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

        d[str(chat_id)] = uname

        with open('activeSessions' ,'w') as storageFile:
            json.dump(d, storageFile)
    except Exception as e:
        print("ERROR save_chat_id(): {0}".format(e))

if locale.getlocale()[0] == 'es_ES':
    if datetime.datetime.today() > endtime:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'ayuda': _('Gives you information about the available commands'),
                      'mejores n': _('Lists n top rated films'),
                      'mejores10': _('Lists top 10 rated films'),
                      'mispuntuaciones': _('Lists your rated films'),
                      'misestadisticas': _('Lists your stats')
        }
    else:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'ayuda': _('Gives you information about the available commands'),
                      'inicio': _('Get used to the bot'),
                      'hoy': _('Shows films for the current day'),
                      'mañana': _('Shows films for tomorrow'),
                      'mejores n': _('Lists n top rated films'),
                      'mejores10': _('Lists top 10 rated films'),
                      'mispuntuaciones': _('Lists your rated films'),
                      'misestadisticas': _('Lists your stats')
        }
elif locale.getlocale()[0] == 'gl_ES':
    if datetime.datetime.today() > endtime:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'axuda': _('Gives you information about the available commands'),
                      'mellores n': _('Lists n top rated films'),
                      'mellores10': _('Lists top 10 rated films'),
                      'asmiñaspuntuacións': _('Lists your rated films'),
                      'asmiñasestatísticas': _('Lists your stats')
        }
    else:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'axuda': _('Gives you information about the available commands'),
                      'inicio': _('Get used to the bot'),
                      'hoxe': _('Shows films for the current day'),
                      'mañá': _('Shows films for tomorrow'),
                      'mellores n': _('Lists n top rated films'),
                      'mellores10': _('Lists top 10 rated films'),
                      'asmiñaspuntuacións': _('Lists your rated films'),
                      'asmiñasestatísticas': _('Lists your stats')
        }
else:
    if datetime.datetime.today() > endtime:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'help': _('Gives you information about the available commands'),
                      'top n': _('Lists n top rated films'),
                      'top10': _('Lists top 10 rated films'),
                      'myrates': _('Lists your rated films'),
                      'mystats': _('Lists your stats')
        }
    else:
        commands = {  # command description used in the "help" command ordered alphabetically
                      'help': _('Gives you information about the available commands'),
                      'start': _('Get used to the bot'),
                      'today': _('Shows films for the current day'),
                      'tomorrow': _('Shows films for tomorrow'),
                      'top n': _('Lists n top rated films'),
                      'top10': _('Lists top 10 rated films'),
                      'myrates': _('Lists your rated films'),
                      'mystats': _('Lists your stats')
        }

markup = tb.types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = tb.types.KeyboardButton(_('/start'))
itembtn2 = tb.types.KeyboardButton(_('/help'))
itembtn3 = tb.types.KeyboardButton(_('/today'))
itembtn4 = tb.types.KeyboardButton(_('/tomorrow'))
itembtn5 = tb.types.KeyboardButton(_('/top10'))
itembtn6 = tb.types.KeyboardButton(_('/myrates'))
itembtn7 = tb.types.KeyboardButton(_('/mystats'))

if datetime.datetime.today() > endtime:
    markup.add(itembtn2, itembtn5, itembtn6, itembtn7)
else:
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

# proxy_url = "http://proxy.server:3128"
# urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):

    #print(call)
    #print("FUNCTION: {0} : USER: {1}".format('test_callback',call.from_user.username))
    logging.info('USER:{0} COMMAND:{1}'.format(call.from_user.id,'test_callback()'))

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
    '''This handler shows a welcome message.'''

    #welcome_message = "{0} {1}. {2}".format(_("Hello"),message.from_user.first_name,_("Howdy!"))
    #bot.reply_to(message, welcome_message)

    chat_id = message.chat.id
    #print("FUNCTION: {0} : USER: {1}".format('send_welcome',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'send_welcome()'))

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
    #print("FUNCTION: {0} : USER: {1}".format('aFilm',message.chat.id))
    chat_id = message.chat.id
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'filmDetail()'))

    films = load_from_JSON()

    theFilm = _("No film found")
    for film in films:
        for session in film.sessions:
            if '/fid_'+session.id[:6] == message.text:
                theFilm = film.toDetail(session.date)
                thePoster = film.poster
                theFilmId = film.id
                theFilmRates = film.rates
                break
    print(theFilmRates)
    voters = [x[0] for x in theFilmRates] if len(theFilmRates) > 0 else None
    if voters is None or chat_id not in voters:
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
        if datetime.datetime.today() > endtime:
            bot.send_photo(chat_id, thePoster)
        else:
            bot.send_photo(chat_id, thePoster, caption = caption, reply_markup=voteKeyboard)

    else:
        bot.reply_to(message, theFilm, parse_mode='HTML')
        bot.send_photo(chat_id, thePoster)
# help
@bot.message_handler(commands=['help','axuda','ayuda'])
def command_help(message):
    '''
    Display the commands and what are they intended for.
    '''
    chat_id = message.chat.id
    #print("FUNCTION: {0} : USER: {1}".format('command_help',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'help()'))

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
    #print("FUNCTION: {0} : USER: {1}".format('command_today',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_today()'))

    if datetime.datetime.today() > endtime:
        bot.send_message(chat_id,_('Cineuropa 2017 is over. Please try another command.'))
    else:
        day = datetime.date.today().day
        films = load_from_JSON()

        ulistaEventos = []
        timeList = []
        for film in films:
            for y in film.sessions:
                if str(day) in y.date.split(' '):
                    ulistaEventos.append(film)
                    timeList.append(y.time)

        if len(ulistaEventos) == 0:
            listaEventos = [_("No sessions today")]
        else:
            timeIndexes = sorted(range(len(timeList)), key=lambda k: timeList[k])
            listaEventos = [ulistaEventos[tInd].toSimple('Día {0} de novembro'.format(day)) for tInd in timeIndexes]

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
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_tomorrow()'))

    if datetime.datetime.today() > endtime:
        bot.send_message(chat_id,_('Cineuropa 2017 is over. Please try another command.'))
    else:
        tomorrow = datetime.date.today()+datetime.timedelta(days=1)
        day = tomorrow.day

        films = load_from_JSON()

        ulistaEventos = []
        timeList = []
        for film in films:
            for y in film.sessions:
                if str(day) in y.date.split(' '):
                    ulistaEventos.append(film)
                    timeList.append(y.time)

        if len(ulistaEventos) == 0:
            listaEventos = [_("No sessions tomorrow")]
        else:
            timeIndexes = sorted(range(len(timeList)), key=lambda k: timeList[k])
            listaEventos = [ulistaEventos[tInd].toSimple('Día {0} de novembro'.format(day)) for tInd in timeIndexes]

        for ev in listaEventos:
            bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# any day
@bot.message_handler(commands=['day','día'])
def command_day(message):

    '''
    Show films of a given day (numeric).
    '''
    chat_id = message.chat.id

    #print("FUNCTION: {0} : USER: {1}".format('command_day',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_day()'))

    if datetime.datetime.today() > endtime:
        bot.send_message(chat_id,_('Cineuropa 2017 is over. Please try another command.'))
    else:
        if len(message.text.split(" ")) > 1:
            day = message.text.split(" ")[1]
            films = load_from_JSON()

            ulistaEventos = []
            timeList = []
            for film in films:
                for y in film.sessions:
                    if str(day) in y.date.split(' '):
                        ulistaEventos.append(film)
                        timeList.append(y.time)

            if len(ulistaEventos) == 0:
                listaEventos = [_("No sessions this day")]
            else:
                timeIndexes = sorted(range(len(timeList)), key=lambda k: timeList[k])
                listaEventos = [ulistaEventos[tInd].toSimple('Día {0} de novembro'.format(day)) for tInd in timeIndexes]

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
    #print("FUNCTION: {0} : USER: {1}".format('command_top',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_top()'))

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
    #print("FUNCTION: {0} : USER: {1}".format('command_top10',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_top10()'))

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

@bot.message_handler(commands=['myrates','mispuntuaciones','asmiñaspuntuacions'])
def command_myrates(message):
    '''Show user's rates'''
    chat_id = message.chat.id
    #print("FUNCTION: {0} : USER: {1}".format('command_myrates',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_myrates()'))

    if len(message.text.split(" ")) == 1:
        films = load_from_JSON()
        myRatedList = [x for x in films if chat_id in [y[0] for y in x.rates]]
        pairs = []
        for ratedFilm in myRatedList:
            for rate in ratedFilm.rates:
                if rate[0] == chat_id:
                    pairs.append((rate[1], ratedFilm.title))

        returnMessage = "********** {0} **********\n".format(_('MY RATES'))
        if len(pairs) > 0:
            sortedList = sorted(pairs, key = lambda x: x[0], reverse=True)
            for elem in sortedList:
                returnMessage += "<b>{0}:</b>{1}\n".format(elem[0], elem[1])
        else:
            returnMessage += _("You haven't rated any film.")
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['myratedfilms','mispeliculaspuntuadas','asmiñaspeliculaspuntuadas'])
def command_myratedfilms(message):
    '''Show user's rated films'''
    chat_id = message.chat.id
    #print("FUNCTION: {0} : USER: {1}".format('command_myratedfilms',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_myratedfilms()'))

    if len(message.text.split(" ")) == 1:
        sessions = load_from_JSON()
        sortedList = sorted([x for x in sessions if chat_id in [y[0] for y in x.rates]], key = lambda x: x.rate, reverse=True)
        returnMessage = "****** {0} ******\n".format(_('MY RATED FILMS'))
        if len(sortedList) > 0:
            listaEventos = [x.toTopListHTML() for x in sortedList]
            for i in range(len(listaEventos)):
                returnMessage += "{0}".format(listaEventos[i])
        else:
                returnMessage += _("You haven't rated any film.")
        bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['search','buscar'])
def command_search(message):
    '''Search in film title'''
    chat_id = message.chat.id
    #print("FUNCTION: {0} : USER: {1}".format('command_myvotes',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_myvotes()'))

    if len(message.text.split(" ")) > 1:

        search_text = " ".join(message.text.split(" ")[1:])
        print(search_text.upper())
        films = load_from_JSON()
        filmsMatch = [x for x in films if search_text.upper() in x.title.upper()]
        if len(filmsMatch) > 0:
            returnMessageItems = []
            day = datetime.date.today().day
            for fm in filmsMatch:
                print(fm.title)
                filmNextSessions = [x for x in fm.sessions if int(x.date.split(" ")[1]) >= day]
                returnMessageItems.append('/fid_'+filmNextSessions[0].id[:6]+' :: '+fm.title)
            bot.send_message(chat_id, "\n".join(returnMessageItems))
        else:
            bot.send_message(chat_id, _("No matches found for upcoming sessions."))
            # bot.send_message(chat_id, fm.toSimple('Día {0} de novembro'.format(day)), parse_mode='HTML')
        # returnMessage = "********** {0} **********\n".format(_('MY RATINGS'))
        # if len(sortedList) > 0:
        #     listaEventos = [x.toTopListHTML() for x in sortedList]
        #     for i in range(len(listaEventos)):
        #         returnMessage += "{0}".format(listaEventos[i])
        # else:
        #         returnMessage += _("You haven't rated any film.")
        # bot.send_message(chat_id, returnMessage, parse_mode='HTML')

    else:
        bot.send_message(chat_id, _("Invalid command"))

@bot.message_handler(commands=['mystats','misestadisticas','asmiñasestatisticas'])
def command_mystats(message):
    '''Show user statistics'''
    chat_id = message.chat.id

    #print("FUNCTION: {0} : USER: {1}".format('command_mystats',chat_id))
    logging.info('USER:{0} COMMAND:{1}'.format(chat_id,'command_mystats()'))

    films = load_from_JSON()
    myfilms = []
    for film in films:
        for rate in film.rates:
            if rate[0] == chat_id:
                myfilms.append((film.id,film.title,rate[1]))

    if len(myfilms) > 0:
        mymax = 0.0
        mymin = 10.0
        mysum = 0.0
        for myfilm in myfilms:
            if float(myfilm[2]) > mymax:
                mymax = float(myfilm[2])
            if float(myfilm[2]) < mymin:
                mymin = float(myfilm[2])
            mysum += float(myfilm[2])
        myavg =  mysum/len(myfilms)
        statsText =  "<b>***** My stats *****</b>\n<b>Films rated:</b> {0}\n<b>Max rating:</b> " \
        "{1}\n<b>Min rating:</b> {2}\n<b>Average rating:</b> {3}".format(len(myfilms),
        mymax, mymin, myavg)
    else:
        statsText = "No films rated."
    bot.send_message(chat_id, statsText, parse_mode='HTML')

@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
    #logging.info('QUERYID:{0} COMMAND:{1}'.format(inline_query.id,'default_query()'))
    logging.info('ID:{0} COMMAND:{1}'.format(inline_query.from_user.id,'default_query()'))

    try:
        day = datetime.date.today().day
        hour = datetime.datetime.now().time().hour
        films = load_from_JSON()
        ulistaEventos = []
        timeList = []
        for film in films:
            for y in film.sessions:
                if str(day) in y.date.split(' ') and (str(hour) <= y.time.split(':')[0]):
                    ulistaEventos.append(film)
                    timeList.append(y.time)

        resultados = []
        if len(ulistaEventos) == 0:
            resultados.append(tb.types.InlineQueryResultCachedSticker('1',
            'CAADAgADFQADyIsGAAHPdbDyCcpB8gI',
            input_message_content=tb.types.InputTextMessageContent(_('Sorry, there are no films today'))))
        else:

            ind = 0
            timeIndexes = sorted(range(len(timeList)), key=lambda k: timeList[k])
            for tInd in timeIndexes:
                ind += 1
                aFilm = ulistaEventos[tInd]
                theSession = aFilm.get_session_from_day(day)
                messageToSend = "<b>{0} ({1})</b>\n".format(aFilm.title, aFilm.year)
                messageToSend += theSession.time + " - " + theSession.place + "\n" + aFilm.synopsis
                resultados.append(tb.types.InlineQueryResultArticle(str(ind),
                    "{0} ({1})".format(aFilm.title, aFilm.year),
                    # tb.types.InputTextMessageContent(aFilm.toSimple('Día {0} de novembro'.format(day)), parse_mode='HTML'),
                    tb.types.InputTextMessageContent(messageToSend, parse_mode='HTML'),
                    reply_markup=None,
                    url=aFilm.url,
                    hide_url=True,
                    description=theSession.time + " - " + theSession.place + "\n" + aFilm.synopsis,
                    thumb_url=aFilm.poster,
                    thumb_width=640,
                    thumb_height=640)
                    )
        bot.answer_inline_query(inline_query.id, resultados)
    except Exception as e:
        print("ERRO: {0}".format(e))
on_start('activeSessions')

#bot.polling()
bot.polling(none_stop=False)
