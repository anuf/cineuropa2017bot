# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import PyPDF2
import re

import telebot as tb
import requests

from cineuropa2017_token import TOKEN

import gettext
import time
import datetime

t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

bot = tb.TeleBot(TOKEN)

commands = {  # command description used in the "help" command ordered alphabetically
              'day n': _('Shows films from a given day'),
              'help': _('Gives you information about the available commands'),
              'start': _('Get used to the bot'),
              'today': _('Shows films for the current day'),
              'tomorrow': _('Shows films for tomorrow')
}

total = []
#proxy_url = "http://proxy.server:3128"
#urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30)
class _Film(object):
    def __init__(self, day, place, hour, title, director):
        self.day = day
        self.place = place
        self.hour = hour
        self.title = title
        self.director = director

    def show(self):
        return "{0}: {1}\n{2}: {3}\n{4}: {5}\n{6}: {7}\n{8}: {9}".format(_("DAY"),self.day,_("PLACE"), self.place, _("TIME"), self.hour, _("TITLE"), self.title, _("DIRECTOR"), self.director)

    def toHTML(self):
        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}".format(_("Title"), self.title, _("Director"), self.director, _("Day"), self.day,_("Time"), self.hour, _("Place"), self.place)

def cleanContent(pageContent):
    returnList = []
    for elem in pageContent:
        if 'CINEUROPA31' in elem:
            print("CINE")
        elif len(elem) == 0:
            print("ZERO")
        elif elem == ' | PROGRAMA':
            print("PROG")
        else:
            returnList.append(elem)

    return returnList

# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''This handlert shows a welcome message.'''
    welcome_message = _("Howdy!")
    load_data()
    bot.reply_to(message, welcome_message)

# help
@bot.message_handler(commands=['help'])
def command_help(message):
    '''
    Display the commands and what are they intended for.
    '''
    chat_id = message.chat.id
    help_text = _("The following commands are available: \n")
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text) # send the generated help page

# today
@bot.message_handler(commands=['today'])
def command_today(message):
    '''
    Show today's films.
    '''

    chat_id = message.chat.id
    day = datetime.date.today().day
    load_data()
    listaEventos = [x.toHTML() for x in total if day in x.day.split(' ')]
    if len(listaEventos) == 0:
        listaEventos = [_("No films today")]
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
    listaEventos = [x.toHTML() for x in total if day in x.day.split(' ')]
    if len(listaEventos) == 0:
        listaEventos = [_("No events tomorrow")]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')

# any day
@bot.message_handler(commands=['day'])
def command_day(message):
    '''
    Show films of a given day (numeric).
    '''

    chat_id = message.chat.id
    day = message.text.split(" ")[1]
    load_data()
    listaEventos = [x.toHTML() for x in total if day in x.day.split(' ')]
    for ev in listaEventos:
        bot.send_message(chat_id, "\n********** {0} **********\n{1}".format(_("FILM"), ev), parse_mode='HTML')


def load_data():
    '''Parses some sheets from official PDF file.'''
    pdfFileObj = open('C31.pdf','rb')     #'rb' for read binary mode
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages

    days = ('LUNS', 'MARTES', 'MÉRCORES', 'XOVES','VENRES','SÁBADO', 'DOMINGO')
    places = ('SEDE AFUNDACIÓN','CINEMA NUMAX', 'CGAC','TEATRO PRINCIPAL', 'SALÓN TEATRO', 'MULTICINES COMPOSTELA (SALA 2)')
    pageContent = []
    for iPage in range(7):#range(numPages):
        pageObj = pdfReader.getPage(iPage)
        pageText = pageObj.extractText().split("\n")
        pageContent += pageText

    #print(pageText)
    filmDays = []
    indexDay = []

    print("LEN1 = "+str(len(pageContent)))
    pageContent = cleanContent(pageContent)
    print("LEN2 = "+str(len(pageContent)))
    for elem in pageContent:
        if elem.split(' ')[0].upper() in days:
            filmDays.append(elem)
            indexDay.append(pageContent.index(elem))
    indexDay.append(len(pageContent))

    print("@"*10)

    for j in range(len(indexDay)-1):
        aday = pageContent[indexDay[j]:indexDay[j+1]]
        # print(aday)
        # print(len(aday))
        contents = " ".join(aday[1:])
        print("+"*10)
        myday = filmDays[j]
        print("DAY: "+myday)
        print("+"*10)
        #print(contents)

        sor = sorted([contents.find(x) for x in places if contents.find(x) != -1])
        sor.append(len(contents))
        # print(sor)
        for i in range(len(sor)-1):
            aplace = contents[sor[i]:sor[i+1]]
            print(" --- "+ aplace)
            for k in places:
                if aplace.find(k) != -1:
                    myplace = k
                    print("PL: ",myplace)
            eventos = aplace.replace(myplace,"").replace("  "," ").strip()

            h = re.findall('\d{2}:\d{2}',eventos)
            f = re.split('\d{2}:\d{2}',eventos)[1:]
            myeventos =  [x[0].strip()+" "+x[1].strip() for x in zip(h,f)] if h is not None else None

            for myev in myeventos:
                ttl = []
                name = []
                for fi2 in myev.split(" "):
                    if re.search('\d{2}:\d{2}',fi2):
                        hora = re.search('\d{2}:\d{2}',fi2).group()
                    elif fi2.istitle():
                        ttl.append(fi2)
                    else:
                        name.append(fi2)
                aFilm = _Film(myday, myplace, hora, " ".join(name), " ".join(ttl))
                aFilm.show()
                total.append(aFilm)
                print("+"*10)
    print(len(total))
    print(total[0].show())
    print(total[1].show())

bot.polling()
