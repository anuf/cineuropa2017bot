# -*- coding: utf-8 -*-

import gettext

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

    def __init__(self, id ='', title='', year='',director='', poster = '', sypnosis = '', rate=None, sessions = []):
        self.id = id
        self.title = title
        self.year = year
        self.director = director
        self.poster = poster
        self.rate = rate
        self.sessions = sessions
        self.sypnosis = sypnosis

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

        # print([x.date for x in self.sessions])
        theSession = [x for x in self.sessions if x.date == aDate][0]

        nextSessions = ", ".join([x.date for x in self.sessions if x.date.split(" ")[1] > aDate.split(" ")[1]])

        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}\n<b>{14}:</b> {15}".format(_("Title"), self.title +" ("+self.year+")",
            _("Director"), self.director, _("Day"), theSession.date ,_("Time"), theSession.time,
            _("Place"), theSession.place, _("Rate"), self.rate, _("Next sessions"), nextSessions,
            _("More..."), "/fid_"+self.id[0:6])

    def toHTML(self):
        # Calculate next sessions to show

        # Return value
        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}".format(_("Title"), self.title,
            _("Director"), self.director, _("Day"), self.day,_("Time"), self.time,
            _("Place"), self.place, _("Rate"), self.rate, _("Next sessions"), self.nextSessions,
            _(""), "/fid_"+self.id
            )
    #
    # def toTopListHTML(self):
    #     return "<b>{0}:</b> {1}\n".format(self.rate, self.title)

    def toDict(self):
        return {"id" : self.id, "title" : self.title, "year" : self.year, "director" : self.director,
            "poster" : self.poster, "sypnosis": self.sypnosis, "rate" : self.rate,
            "sessions": [x.toDict() for x in self.sessions]}
