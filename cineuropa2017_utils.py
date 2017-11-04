# -*- coding: utf-8 -*-

import PyPDF2
import re
from film import Film
import json
import gettext
from film import Film

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
        print("parsePDFprogram "+str(iPage))
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
                aFilm = Film(day = myday, place = myplace, time = hora, title=" ".join(name), director =" ".join(ttl))
                aFilm.show()
                total.append(aFilm)
                #print("+"*10)

    # Fill next sessions field before saving
    for t1 in total:
        nextList = []
        for t2 in total:

            if t1.title == t2.title and t1.day.split(" ")[1] < t2.day.split(" ")[1]:
                print("pasa {0} ::: {1}".format(t1.day, t2.day))
                nextList.append(t2.day)

        t1.setNextSessions(', '.join(nextList))

    # Save sessions to file
    with open('films.json', 'w') as outputFile:
        json.dump([elem.toDict() for elem in total], outputFile)
        # for elem in total:
        #     json.dump(elem.toDict(), outputFile, indent=4)
    load_sessions()

def load_sessions():
    '''
    Load JSON file where sessions are stored and creates list of Film objects.
    '''
    with open('films.json', 'r') as inputFile:
        d = json.load(inputFile)
    return [object2film(x) for x in d]

def object2film(anObject):
    '''Convert an json object into a Film'''
    return Film(anObject['day'], anObject['place'], anObject['time'], anObject['title'],
anObject['director'], anObject['rate'], anObject['next'])
