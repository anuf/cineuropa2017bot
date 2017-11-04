# -*- coding: utf-8 -*-

import gettext

t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

class Film(object):
    def __init__(self, day='', place='', time='', title='', director='', rate = '', nextSessions = ''):
        self.day = day
        self.place = place
        self.time = time
        self.title = title
        self.director = director
        self.rate = rate
        self.nextSessions = nextSessions

    def setNextSessions(self, aString):
        self.nextSessions = aString

    def show(self):
        return "{0}: {1}\n{2}: {3}\n{4}: {5}\n{6}: {7}\n{8}: {9}\n{10}: {11}\n{12}: {13}".format(
    _("DAY"), self.day, _("PLACE"), self.place, _("TIME"), self.time,
    _("TITLE"), self.title, _("DIRECTOR"), self.director, _("RATE"), self.rate,
    _("NEXT SESSIONS"), self.nextSessions)

    def toHTML(self):
        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}\n<b>{10}:</b> {11}\n<b>{12}:</b> {13}".format(_("Title"), self.title,
    _("Director"), self.director, _("Day"), self.day,_("Time"), self.time,
    _("Place"), self.place, _("Rate"), self.rate, _("Next sessions"), self.nextSessions)

    def toDict(self):
        return {"day":self.day, "place":self.place, "time":self.time, "title": self.title,
    "director": self.director, "rate": self.rate, "next": self.nextSessions}
