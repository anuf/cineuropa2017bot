# -*- coding: utf-8 -*-

import gettext

t = gettext.translation(
    'cineuropa2017', 'locale',
    fallback=True,
)
_ = t.gettext

class Film(object):
    def __init__(self, day='', place='', time='', title='', director=''):
        self.day = day
        self.place = place
        self.time = time
        self.title = title
        self.director = director

    def show(self):
        return "{0}: {1}\n{2}: {3}\n{4}: {5}\n{6}: {7}\n{8}: {9}".format(_("DAY"),self.day,_("PLACE"), self.place, _("TIME"), self.time, _("TITLE"), self.title, _("DIRECTOR"), self.director)

    def toHTML(self):
        return "<b>{0}:</b> {1}\n<b>{2}:</b> {3}\n<b>{4}:</b> {5}\n<b>{6}:</b> {7}\n<b>{8}:</b> {9}".format(_("Title"), self.title, _("Director"), self.director, _("Day"), self.day,_("Time"), self.time, _("Place"), self.place)

    def toDict(self):
        return {"day":self.day, "place":self.place, "time":self.time, "title": self.title, "director": self.director}
