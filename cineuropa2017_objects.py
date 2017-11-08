# -*- coding: utf-8 -*-

import gettext
import datetime

t = gettext.translation(
    'film', 'locale',
    fallback=True,
)
_ = t.gettext

class SessionObject(object):
    def __init__(self, anId ='', aDate='', aPlace='', aTime=''):
        self.id = anId
        self.date = aDate
        self.place = aPlace
        self.time = aTime

    def toString(self):
        return "ID: {0}\nDATE: {1}\nPLACE: {2}\nTIME: {3}".format(self.id, self.date, self.place, self.time)

    def toDict(self):
        return {"id" : self.id, "date" : self.date, "place" : self.place,
            "time" : self.time}

class FilmObject(object):

    def __init__(self, id ='', title='', year='',director='', poster = '',
        synopsis = '', duration = '', rate=None, rates = [], sessions = [],
        url = '', gender = '', countries = ''):
        self.id = id
        self.title = title
        self.year = year
        self.director = director
        self.poster = poster
        self.rate = rate
        self.rates = rates
        self.sessions = sessions
        self.synopsis = synopsis
        self.duration = duration
        self.url = url
        self.gender = gender
        self.countries = countries

    def addSession(self, aSession):
        self.sessions.append(aSession)

    def setSessions(self, aListOfSessions):
        self.sessions = aListOfSessions

    def setRate(self, aRate):
        self.rate = aRate

    def getId(self):
        return self.id

    # def show(self):
    #     return "{0}: {1}\n{2}: {3}\n{4}: {5}\n{6}: {7}\n{8}: {9}\n{10}: {11}\n{12}: {13}".format(
    # _("DAY"), self.day, _("PLACE"), self.place, _("TIME"), self.time,
    # _("TITLE"), self.title, _("DIRECTOR"), self.director, _("RATE"), self.rate,
    # _("NEXT SESSIONS"), self.nextSessions)
    #
    def toSimple(self, aDate):
        # A film only is shown in a session at a given day
        # TODO: Add Poster
        days = ('Luns', 'Martes', 'Mércores', 'Xoves','Venres','Sábado', 'Domingo')
        # print([x.date for x in self.sessions])
        theSession = [x for x in self.sessions if x.date == aDate][0]

        nextSessionsList = [x.date for x in self.sessions if int(x.date.split(" ")[1]) > int(aDate.split(" ")[1])]

        sList = []
        for x in nextSessionsList:
            x_splited = x.split(" ")[1:]
            dtx = datetime.date(2017, 11, int(x_splited[0]))
            xList = [days[datetime.date.weekday(dtx)]]
            for y in x_splited:
                xList.append(y)
            sList.append(" ".join(xList))
        nextSessions = ', '.join(sList)


        splitedDate = theSession.date.split(" ")[1:]
        dt = datetime.date(2017, 11, int(splitedDate[0]))
        theDateList = [days[datetime.date.weekday(dt)]]
        for x in splitedDate:
            theDateList.append(x)

        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}\n<b>{14}:</b> {15}".format(_("Title"), self.title +" ("+self.year+")",
            _("Director"), self.director, _("Day"), " ".join(theDateList) ,_("Time"), theSession.time,
            _("Place"), theSession.place, _("Rate"), self.rate, _("Next sessions"), nextSessions,
            _("More"), "/fid_"+theSession.id[0:6])

    def toDetail(self, aDate):
        # A film only is shown in a session at a given day
        # TODO: Add Poster

        # print([x.date for x in self.sessions])
        theSession = [x for x in self.sessions if x.date == aDate][0]

        nextSessions = ", ".join([x.date for x in self.sessions if x.date.split(" ")[1] > aDate.split(" ")[1]])

        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}\n<b>{14}:</b> {15}".format(
                _("Title"), self.title +" ("+self.year+")",
                _("Director"), self.director, _("Day"), theSession.date ,
                _("Time"), theSession.time, _("Place"), theSession.place,
                _("Rate"), self.rate, _("Next sessions"), nextSessions,
                _("Synopsis"), self.synopsis)

    def toHTML(self):
        # Calculate next sessions to show

        # Return value
        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}".format(_("Title"), self.title,
            _("Director"), self.director, _("Day"), self.day,_("Time"), self.time,
            _("Place"), self.place, _("Rate"), self.rate, _("Next sessions"), self.nextSessions,
            _("More"), "/fid_"+self.id
            )
    #
    # def toTopListHTML(self):
    #     return "<b>{0}:</b> {1}\n".format(self.rate, self.title)

    def toDict(self):
        return {"id" : self.id, "title" : self.title, "year" : self.year,
            "director" : self.director, "poster" : self.poster,
            "synopsis": self.synopsis, "duration" : self.duration,
            "rate" : self.rate, "rates" : self.rates,
            "sessions" : [x.toDict() for x in self.sessions],
            "url" : self.url, "gender" :  self.gender, "countries" : self.countries
            }
