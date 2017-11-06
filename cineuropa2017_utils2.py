# -*- coding: utf-8 -*-

#import requests
from bs4 import BeautifulSoup
#import urllib3

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
    'cineuropa2017', 'locale',
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

def parsePDFprogram():
    '''
    Parse some sheets from official PDF file.
    Stores film sessions in JSON format.
    '''

    total = []
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

    #print("LEN1 = "+str(len(pageContent)))
    pageContent = cleanContent(pageContent)
    #print("LEN2 = "+str(len(pageContent)))
    for elem in pageContent:
        if elem.split(' ')[0].upper() in days:
            filmDays.append(elem)
            indexDay.append(pageContent.index(elem))
    indexDay.append(len(pageContent))

    #print("@"*10)

    for j in range(len(indexDay)-1):
        aday = pageContent[indexDay[j]:indexDay[j+1]]
        # print(aday)
        # print(len(aday))
        contents = " ".join(aday[1:])
        #print("+"*10)
        myday = filmDays[j]
        #print("DAY: "+myday)
        #print("+"*10)
        #print(contents)

        sor = sorted([contents.find(x) for x in places if contents.find(x) != -1])
        sor.append(len(contents))
        # print(sor)
        for i in range(len(sor)-1):
            aplace = contents[sor[i]:sor[i+1]]
            #print(" --- "+ aplace)
            for k in places:
                if aplace.find(k) != -1:
                    myplace = k
                    #print("PL: ",myplace)
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
                aFilm = Film(day = myday, place = myplace, time = hora,
                title=" ".join(name), director =" ".join(ttl), rate = random.randint(0,100))
                aFilm.show()
                total.append(aFilm)
                #print("+"*10)

    # Fill next sessions field before saving
    for t1 in total:
        nextList = []
        for t2 in total:
            if t1.title == t2.title and t1.day.split(" ")[1] < t2.day.split(" ")[1]:
                nextList.append(t2.day)

        t1.setNextSessions(', '.join(nextList))

    # Save sessions to file
    with open('films.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in total], outputFile)
        # for elem in total:
        #     json.dump(elem.toDict(), outputFile, indent=4)
    load_sessions()

def parsePDFprogram2():
    '''
    Parse some sheets from official PDF file.
    Stores film sessions in JSON format.
    '''

    total = []
    total2 = []
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

    filmDays = []
    indexDay = []

    # Clean content
    pageContent = cleanContent(pageContent)

    # Extract days and index on total content
    for elem in pageContent:
        if elem.split(' ')[0].upper() in days:
            filmDays.append(elem)
            indexDay.append(pageContent.index(elem))
    # Append an extra index for search intervals
    indexDay.append(len(pageContent))

    # loop on days
    for j in range(len(indexDay)-1):
        aday = pageContent[indexDay[j]:indexDay[j+1]]

        # All contents from a day as a string
        contents = " ".join(aday[1:])
        # Selected day
        myday = filmDays[j]

        # Extract (ordered) indexes of places
        sor = sorted([contents.find(x) for x in places if contents.find(x) != -1])
        # Append an extra index for search intervals
        sor.append(len(contents))
        # loop on places occurrences
        for i in range(len(sor)-1):
            # Extract contents for a place
            aplace = contents[sor[i]:sor[i+1]]
            # Search in places
            for k in places:
                # If place exists in subcontents, extract it
                if aplace.find(k) != -1:
                    myplace = k
            # Extract sessions cleanning double empty spaces
            eventos = aplace.replace(myplace,"").replace("  "," ").strip()

            # Extract time
            h = re.findall('\d{2}:\d{2}',eventos)
            # Extract subcontents but time
            f = re.split('\d{2}:\d{2}',eventos)[1:]
            myeventos =  [x[0].strip()+" "+x[1].strip() for x in zip(h,f)] if h is not None else None
            # Loop in sessions
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
                aFilm = Film(day = myday, place = myplace, time = hora,
                title=" ".join(name), director =" ".join(ttl), rate = random.randint(0,100))
                aFilm.show()
                total.append(aFilm)

                # SESSION OBJECT
                ssObjectIdString = myday+myplace+hora
                ssObjectId = hashlib.md5(ssObjectIdString.encode('utf-8')).hexdigest()
                print("ssObjectId: {0}".format(ssObjectId))
                so = SessionObject(ssObjectId, myday, myplace, hora)
                print(so.toString())

                filmObjectIdString = " ".join(name)
                filmObjectId = hashlib.md5(filmObjectIdString.encode('utf-8')).hexdigest()
                print("filmObjectId: {0}".format(filmObjectId))
                # Check if filmObject already exits. If so, update. Else add it to list

                if filmObjectId not in [x.id for x in total2]:
                    fo = FilmObject(id=filmObjectId, title=filmObjectIdString,
                        director=" ".join(ttl), poster = '', rate=random.randint(0,100),
                        sessions = [so])
                    total2.append(fo)
                else:
                    indexFilmObject = [x.id for x in total2].index(filmObjectId)
                    fo = total2[indexFilmObject]
                    fo.addSession(so)
            print("*"*50)
            print(total2[0])

    # Save sessions to file
    with open('films2.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in total2], outputFile)
        # for elem in total:
        #     json.dump(elem.toDict(), outputFile, indent=4)
    print("TOTAL2 : {0}".format(len(total2)))
    print("\n".join([x.title for x in total2]))

    print([x.toSimple("Martes 7 de novembro") for x in total2 if x.id == "ff2f94e9859cb0cdbe006d55eb21285c"])

def load_sessions2():
    '''
    Load JSON file where sessions are stored and creates list of Film objects.
    '''
    with open('allfilms2.json', 'r') as inputFile:
        d = json.load(inputFile)
    print(d[-1])
    return [object2film2(x) for x in d]

def object2film2(anObject):
    '''Convert an json object into a Film'''
    sessionsList = [object2session(x) for x in anObject['sessions']]
    return FilmObject(id=anObject['id'], title=anObject['title'], year=anObject['year'],
        director=anObject['director'], poster=anObject['poster'],
        rate=anObject['rate'],
        sessions=sessionsList)

def object2session(anObject):
    '''Convert an json object into a session'''
    return SessionObject(anId=anObject['id'], aDate=anObject['date'],
        aPlace=anObject['place'], aTime=anObject['time'])

# def getNextSessions():
#     # Fill next sessions field before saving
#     for t1 in total:
#         nextList = []
#         for t2 in total:
#             if t1.title == t2.title and t1.day.split(" ")[1] < t2.day.split(" ")[1]:
#                 nextList.append(t2.day)
#
#         t1.setNextSessions(', '.join(nextList))

def parseFromURL(url):
    print("parseFromURL")
    response = urllib3.PoolManager().request('GET', url)

    if response.status == 200:
        print("parseFromURL2")
        soup = BeautifulSoup(response.data, "lxml")
        qq = soup.find_all('div', attrs={'class': 'qq'})
        print("parseFromURL3")
        for q in qq:
            print("parseFromURL4")
            print(qq.find('p').find('a'))
    else:
        print("STATUS: "+str(response.status))

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
        # print(theDay)

        for indPlace in range(len(placeBlocksIndexes)-1):
            placeHTMLText = dayHTMLText[placeBlocksIndexes[indPlace]:placeBlocksIndexes[indPlace+1]]
            soup2 = BeautifulSoup(placeHTMLText, "lxml")
            # Find a place
            aPlace = soup2.find('h4')
            thePlace = aPlace.text
            #print(thePlace)

            # for place in h4:
            #     print(place.text)
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
                titles.append(re.split('\(\d{4}\)',titleYearDirector)[0].strip())
                directors.append(re.split('\(\d{4}\)',titleYearDirector)[1].strip())
                years.append(re.search('\(\d{4}\)',titleYearDirector).group().strip()[1:-1])

                # print("TITLE: {0}".format(title))
                # print("DIRECTOR: {0}".format(director[2:]))
                # print("YEAR: {0}".format(year))

            # posters
            posters = ["http://www.cineuropa.gal/"+x.find("img")["src"] for x in a]

            for i in range(len(times)):

                theTime = times[i][0]
                # SESSION OBJECT
                ssObjectIdString = theDay+thePlace+theTime
                ssObjectId = hashlib.md5(ssObjectIdString.encode('utf-8')).hexdigest()
                #print("ssObjectId: {0}".format(ssObjectId))
                so = SessionObject(ssObjectId, theDay, thePlace, theTime)
                #print(so.toString())

                theTitle = titles[i]
                thePoster = posters[i]
                theDirector = directors[i]
                theYear = years[i]

                filmObjectIdString = theTitle
                filmObjectId = hashlib.md5(filmObjectIdString.encode('utf-8')).hexdigest()
                #print("filmObjectId: {0}".format(filmObjectId))

                # Check if filmObject already exits. If so, update. Else add it to list
                if filmObjectId not in [x.id for x in allfilms]:
                    fo = FilmObject(id=filmObjectId, title=filmObjectIdString, year=theYear,
                        director=theDirector, poster = thePoster, rate=random.randint(0,100),
                        sessions = [so])
                    allfilms.append(fo)
                else:
                    indexFilmObject = [x.id for x in allfilms].index(filmObjectId)
                    fo = allfilms[indexFilmObject]
                    fo.addSession(so)

    # Save sessions to file
    with open('allfilms2.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in allfilms], outputFile)
        # for elem in total:
        #     json.dump(elem.toDict(), outputFile, indent=4)
    # print("ALLFILMS : {0}".format(len(allfilms)))
    # print("\n".join([x.title for x in allfilms]))
    print("OK")

if __name__=="__main__":
    url = 'http://www.cineuropa.gal/2017/programa'
    parseFromTxt("program2.txt")
