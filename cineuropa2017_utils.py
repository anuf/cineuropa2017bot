# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib3
# To avoid 403
from urllib.request import Request, urlopen

#import PyPDF2
import re
#from film import Film
import json
import gettext
#from film import Film
import random
from cineuropa2017_objects import FilmObject, SessionObject
import hashlib
import re
import datetime
import dateutil.parser


t = gettext.translation(
    'cineuropa2017_utils', 'locale',
    fallback=True,
)
_ = t

def parse_duration(duration_str):
    """Parse film duration from string (Cineuropa formtatted)."""
    duration = duration_str.split(' ')[0]
    if duration == '':
        duration = 0
    duration = int(duration)
    return duration


def get_time(time_string):
    """Parse time from string."""
    hh_mm_pattern = (r"""^\s*(?P<hour>\d?\d):(?P<minute>\d?\d)"""
                     """(?P<de_seguido>\s+-\s+DE SEGUIDO)?""")
    hh_mm = re.match(hh_mm_pattern, time_string)
    return hh_mm


def get_end_time(theDay='',
                 theTime='',
                 duration=None,
                 prevEndTime=''):
    """Compute the end time of a session."""
    assert (bool(theDay and theTime and duration is not None)
            != bool(prevEndTime and duration is not None))
    if theDay and theTime and duration is not None:
        hh_mm = get_time(theTime)
        day_int = int(re.match(r"^D.a (\d+)", theDay).groups()[0])
        start_datetime = datetime.datetime(year=2017,
                                           month=11,
                                           day=day_int,
                                           hour=int(hh_mm.group('hour')),
                                           minute=int(hh_mm.group('minute')))
        end_datetime = (start_datetime +
                        datetime.timedelta(minutes=parse_duration(duration)))
    elif prevEndTime and duration is not None:
        end_datetime = (dateutil.parser.parse(prevEndTime) +
                        datetime.timedelta(minutes=parse_duration(duration)))
    return end_datetime.isoformat()


def cleanContent(pageContent):
    '''Remove undesired elements from list'''

    returnList = []
    for elem in pageContent:
        if 'CINEUROPA31' in elem:
            #print("CINE")
            pass
        elif len(elem) == 0:
            #print("ZERO")
            pass
        elif elem == ' | PROGRAMA':
            #print("PROG")
            pass
        else:
            returnList.append(elem)

    return returnList

def load_from_JSON():
    '''
    Load JSON file where sessions are stored and creates list of Film objects.
    '''
    with open('allfilms.json', 'r') as inputFile:
        d = json.load(inputFile)
    #print(_("Sessions loaded"))
    return [object2film(x) for x in d]

def object2film(anObject):
    '''Convert an json object into a Film'''
    sessionsList = [object2session(x) for x in anObject['sessions']]
    ratesList = anObject['rates']
    return FilmObject(id=anObject['id'],
        title=anObject['title'],
        synopsis=anObject['synopsis'],
        #critica_cineuropa = anObject['critica_cineuropa'],
        duration = anObject['duration'],
        year=anObject['year'],
        director=anObject['director'],
        poster=anObject['poster'],
        rate=anObject['rate'],
        rates=ratesList,
        gender = anObject['gender'],
        url = anObject['url'],
        countries = anObject['countries'],
        sessions=sessionsList)


def object2session(anObject):
    '''Convert an json object into a session'''
    return SessionObject(anId=anObject['id'], aDate=anObject['date'],
        aPlace=anObject['place'], aTime=anObject['time'])

def parseFromURL(url):
    #print("parseFromURL")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    synopsis = ''
    info = ''
    if urlopen(req).status == 200:
        # print("*"*80)

        contents = urlopen(req).read()
        rows = re.split('<div class="row">', contents.decode("utf-8"))

        strRows = [str(x) for x in rows[1:]]
        soup1 = BeautifulSoup(strRows[0], "lxml")

        soup2 = BeautifulSoup(strRows[1], "lxml")
        imaxe = "www.cineuropa.gal/"+soup2.find("img")["src"]

        h4s = soup2.find_all('h4')
        info = h4s[0].text
        synopsis = h4s[-1].text

    try:
        soup3 = BeautifulSoup(strRows[2], "lxml")
        h4s3 = soup3.find_all('h4')
        h4s3_title = h4s3[0].text
        critica_cineuropa = h4s3[1].text
    except IndexError:
        critica_cineuropa = ''


    else:
        print("STATUS: "+str(urlopen(req).status))
    return synopsis, info, critica_cineuropa

def parseMainFromURL(url):
    allfilms = []
    print("parseMainFromURL")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    synopsis = ''
    info = ''
    if urlopen(req).status == 200:
        # print("*"*80)

        contents = urlopen(req).read()
        soup0 = BeautifulSoup(contents.decode("utf-8"), "lxml")
        rows = soup0.find_all('div', attrs={'class': 'row'})
        data = str(rows[1])

        # Select days from text
        dayBlocksIndexes = [m.start() for m in re.finditer('<h3', data)]
        dayBlocksIndexes.append(len(data))

        # loop in days
        for indDay in range(len(dayBlocksIndexes)-1):
            dayHTMLText = data[dayBlocksIndexes[indDay]:dayBlocksIndexes[indDay+1]]
            soup1 = BeautifulSoup(dayHTMLText, "lxml")

            # Finda day
            aDay = soup1.find('h3')
            # find all places for a given day
            h4 = soup1.find_all('h4')

            # Select places from text
            placeBlocksIndexes = [m.start() for m in re.finditer('<h4', dayHTMLText)]
            placeBlocksIndexes.append(len(dayHTMLText)-1)#dayHTMLText.rfind('</h4>')+5)

            theDay = aDay.text

            for indPlace in range(len(placeBlocksIndexes)-1):
                placeHTMLText = dayHTMLText[placeBlocksIndexes[indPlace]:placeBlocksIndexes[indPlace+1]]
                soup2 = BeautifulSoup(placeHTMLText, "lxml")
                # Find a place
                aPlace = soup2.find('h4')
                thePlace = aPlace.text

                p = soup2.find_all('p')
                a = soup2.find_all('a')
                h5 = soup2.find_all('h5')

                # print("P: {0} :::  A: {1} ::: H5: {2} for day {3}".format(len(p), len(a), len(h5), theDay))
                # if len(set([len(p), len(a), len(h5)])) != 1:
                #     print("Your maths are wrong!")
                #     sys.out()

                # times
                times = [re.findall('\d{2}:\d{2}|DE SEGUIDO',str(hhmm)) for hhmm in p if 'Nota do público' not in str(hhmm)]

                # Update times with "DE SEGUIDO label, adding last time"
                last_time = ""
                for t in times:
                    if t[0] != 'DE SEGUIDO':
                        last_time = t[0]
                    else:
                        t[0] = " - ".join([last_time, t[0]])
                        last_time = t[0][0:6]

                # titles
                titles = []
                years = []
                directors = []
                for x in h5:
                    titleYearDirector = x.text

                    if re.search("PELÍCULA SORPRESA",titleYearDirector):# == "PELÍCULA SORPRESA– ":
                        titles.append('PELÍCULA SORPRESA')
                        directors.append('')
                        years.append('')
                    else:
                        titles.append(re.split('\(\d{4}\)',titleYearDirector)[0].strip())
                        directors.append(re.split('\(\d{4}\)',titleYearDirector)[1].strip())
                        years.append(re.search('\(\d{4}\)',titleYearDirector).group().strip()[1:-1])

                # posters
                posters = ["http://www.cineuropa.gal/"+x.find("img")["src"] for x in a]
                #
                details = ["http://www.cineuropa.gal/"+x["href"] for x in a]
                # print(details)

                for i in range(len(times)):
                    film_url = details[i]
                    synopsis, info, critica_cineuropa = parseFromURL(film_url)
                    # extract from info
                    gen  = re.search('experimental|videoarte|documental|ficción|drama', info.lower())
                    gender = gen.group() if gen is not None else ''
                    countries = re.sub("-",",", info.split("/")[0]).strip()

                    dur = re.search('/ (\d)* min. /',info)
                    duration = dur.group()[1:-1].strip() if dur is not None else ''
                    theTime = times[i][0]
                    # SESSION OBJECT
                    if 'DE SEGUIDO' in theTime:
                        theStartTime = prevEndTime
                        theEndTime = get_end_time(prevEndTime=prevEndTime,
                                                  duration=duration)
                        ssObjectIdString = theDay+thePlace+theStartTime
                    else:
                        # hack to format theStartTime
                        theStartTime = get_end_time(theDay=theDay,
                                                    theTime=theTime,
                                                    duration='0')
                        theEndTime = get_end_time(theDay=theDay,
                                                  theTime=theTime,
                                                  duration=duration)
                        ssObjectIdString = theDay+thePlace+theTime
                    ssObjectId = hashlib.md5(ssObjectIdString.encode('utf-8')).hexdigest()
                    so = SessionObject(ssObjectId, theDay, thePlace, theTime)

                    theTitle = titles[i]
                    thePoster = posters[i]
                    theDirector = directors[i][1:].strip()
                    theYear = years[i]

                    filmObjectIdString = theTitle
                    filmObjectId = hashlib.md5(filmObjectIdString.encode('utf-8')).hexdigest()

                    # Check if filmObject already exits. If so, update. Else add it to list
                    if filmObjectId not in [x.id for x in allfilms]:
                        fo = FilmObject(id = filmObjectId,
                            title = filmObjectIdString,
                            year = theYear,
                            director = theDirector,
                            poster = thePoster,
                            synopsis = synopsis,
                            critica_cineuropa = critica_cineuropa,
                            duration = duration,
                            rate = 0,
                            rates = [],
                            sessions = [so],
                            url = film_url,
                            gender = gender.capitalize(),
                            countries = countries
                            )
                        allfilms.append(fo)
                    else:
                        indexFilmObject = [x.id for x in allfilms].index(filmObjectId)
                        fo = allfilms[indexFilmObject]
                        fo.addSession(so)
                    prevEndTime = theEndTime

        # Save sessions to file
        with open('updated.json', 'w') as outputFile:
            json.dump([elem.toDict() for elem in allfilms], outputFile, indent=4)

        print("Films stored in updated JSON: OK")
    else:
        print("STATUS: "+str(urlopen(req).status))
    return synopsis, info, critica_cineuropa

def parseFromTxt(aFilename):
    allfilms = []
    with open(aFilename,'r') as inputFile:
        data = inputFile.read()

    # Select days from text
    dayBlocksIndexes = [m.start() for m in re.finditer('<div class="clearfix"></div><h3', data)]
    dayBlocksIndexes.append(data.find('<!-- container -->'))
    #print("{0} days found".format(len(dayBlocksIndexes)-1))
    # loop in days
    for indDay in range(len(dayBlocksIndexes)-1):
        dayHTMLText = data[dayBlocksIndexes[indDay]:dayBlocksIndexes[indDay+1]]
        soup1 = BeautifulSoup(dayHTMLText, "lxml")

        # Finda day
        aDay = soup1.find('h3')
        # find all places for a given day
        h4 = soup1.find_all('h4')

        # Select places from text
        placeBlocksIndexes = [m.start() for m in re.finditer('<h4', dayHTMLText)]
        placeBlocksIndexes.append(len(dayHTMLText)-1)#dayHTMLText.rfind('</h4>')+5)

        theDay = aDay.text

        for indPlace in range(len(placeBlocksIndexes)-1):
            placeHTMLText = dayHTMLText[placeBlocksIndexes[indPlace]:placeBlocksIndexes[indPlace+1]]
            soup2 = BeautifulSoup(placeHTMLText, "lxml")
            # Find a place
            aPlace = soup2.find('h4')
            thePlace = aPlace.text

            p = soup2.find_all('p')
            a = soup2.find_all('a')
            h5 = soup2.find_all('h5')

            #print("P: {0} :::  A: {1} ::: H5: {2}".format(len(p), len(a), len(h5)))
            if len(set([len(p), len(a), len(h5)])) != 1:
                print("Your maths are wrong!")
                sys.out()

            # times
            times = [re.findall('\d{2}:\d{2}|DE SEGUIDO',str(hhmm)) for hhmm in p]
            # titles
            titles = []
            years = []
            directors = []
            for x in h5:
                titleYearDirector = x.text

                if re.search("PELÍCULA SORPRESA",titleYearDirector):# == "PELÍCULA SORPRESA– ":
                    titles.append('PELÍCULA SORPRESA')
                    directors.append('')
                    years.append('')
                else:
                    titles.append(re.split('\(\d{4}\)',titleYearDirector)[0].strip())
                    directors.append(re.split('\(\d{4}\)',titleYearDirector)[1].strip())
                    years.append(re.search('\(\d{4}\)',titleYearDirector).group().strip()[1:-1])

            # posters
            posters = ["http://www.cineuropa.gal/"+x.find("img")["src"] for x in a]
            #
            details = ["http://www.cineuropa.gal/"+x["href"] for x in a]
            # print(details)

            for i in range(len(times)):

                film_url = details[i]
                synopsis, info, critica_cineuropa = parseFromURL(film_url)
                # extract from info
                gen  = re.search('experimental|videoarte|documental|ficción|drama', info.lower())
                gender = gen.group() if gen is not None else ''
                countries = re.sub("-",",", info.split("/")[0]).strip()

                dur = re.search('/ (\d)* min. /',info)
                duration = dur.group()[1:-1].strip() if dur is not None else ''
                theTime = times[i][0]
                # SESSION OBJECT
                ssObjectIdString = theDay+thePlace+theTime
                ssObjectId = hashlib.md5(ssObjectIdString.encode('utf-8')).hexdigest()
                so = SessionObject(ssObjectId, theDay, thePlace, theTime)

                theTitle = titles[i]
                thePoster = posters[i]
                theDirector = directors[i][1:].strip()
                theYear = years[i]

                filmObjectIdString = theTitle
                filmObjectId = hashlib.md5(filmObjectIdString.encode('utf-8')).hexdigest()

                # Check if filmObject already exits. If so, update. Else add it to list
                if filmObjectId not in [x.id for x in allfilms]:
                    fo = FilmObject(id = filmObjectId,
                        title = filmObjectIdString,
                        year = theYear,
                        director = theDirector,
                        poster = thePoster,
                        synopsis = synopsis,
                        critica_cineuropa = critica_cineuropa,
                        duration = duration,
                        rate = 0,
                        rates = [],
                        sessions = [so],
                        url = film_url,
                        gender = gender.capitalize(),
                        countries = countries
                        )
                    allfilms.append(fo)
                else:
                    indexFilmObject = [x.id for x in allfilms].index(filmObjectId)
                    fo = allfilms[indexFilmObject]
                    fo.addSession(so)

    # Save sessions to file
    with open('allfilms_base.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in allfilms], outputFile, indent=4)

    print("Films stored in JSON base: OK")

def update_allfilms():
    '''Updates film sessions with contetnts of the updated.json file'''

    with open('allfilms.json','r') as allfilmsFile:
        allfilms = json.load(allfilmsFile)

    with open('updated.json','r') as updatedFile:
        updated = json.load(updatedFile)

    for u in updated:
        try:
            ind = [x['id'] for x in allfilms].index(u['id'])
            allfilms[ind]['sessions'] = u['sessions']
        except:
            print("NEW FILM FOUND: {0}".format(u['title']))
            allfilms.append(u)

    with open('allfilms.json','w') as outFile:
        json.dump([elem for elem in allfilms], outFile, indent=4)


if __name__=="__main__":
    url = 'http://www.cineuropa.gal/2017/programa'
    # Basic html content on 7/11 from site
    #parseFromTxt("program.txt")
    # Obtain updates from URL to updated.json file
    parseMainFromURL(url)
    # update existing sessions in allfilms.json
    #update_allfilms()
