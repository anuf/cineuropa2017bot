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

t = gettext.translation(
    'cineuropa2017_utils', 'locale',
    fallback=True,
)
_ = t

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
    with open('allfilms5.json', 'r') as inputFile:
        d = json.load(inputFile)
    #print(_("Sessions loaded"))
    return [object2film(x) for x in d]

def object2film(anObject):
    '''Convert an json object into a Film'''
    sessionsList = [object2session(x) for x in anObject['sessions']]
    ratesList = anObject['rates']
    return FilmObject(id=anObject['id'], title=anObject['title'],
        synopsis=anObject['synopsis'], year=anObject['year'],
        director=anObject['director'], poster=anObject['poster'],
        rate=anObject['rate'],rates=ratesList,
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

    else:
        print("STATUS: "+str(urlopen(req).status))
    return synopsis, info

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
                synopsis, info = parseFromURL(film_url)
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
    with open('allfilms5.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in allfilms], outputFile, indent=4)

    print("Films stored in JSON: OK")

if __name__=="__main__":
    url = 'http://www.cineuropa.gal/2017/programa'
    parseFromTxt("program3.txt")
