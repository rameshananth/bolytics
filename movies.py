import requests
from lxml import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Movie
from tqdm import *
import pdb

def sMakeASession(filename):
        #setup the db session
        engine=create_engine('sqlite:///'+filename,echo=False)
        Base.metadata.bind=engine
        DBSession=sessionmaker(bind=engine)
        session=DBSession()
        return session

def isTitle(col):
        if col.text_content()=="Name" or col.text_content()=="Title":
                return True
        else:
                return False

def makeLink(col):
        #print list(col.iterlinks())
        if list(col.iterlinks()):
                return list(col.iterlinks())[0][2]
        else:
                return ''

def checkSpanning(col):
        if col.get('colspan'):
                return True
        else:
                return False

def parseTable(table,year):
        """
        The Wikipedia page on Bollywood movies has multiple formats
        1. Predominantly wikitable with the fields being title,director, genre and cast
        2. Wikitable with the fieds also including data of release which also has variants but limited to the years (2017-2007)
        3. Wikitable with the year available in row 1 mostly in the years 1940-1950 (but why?)
        4. And a few other assorted types
        Each movie in the table also has a link to a page in wikipedia (if someone has bothered to create it)
        We need to save the link too, as that is the only element guaranteed to be unique across the wikipedia namespace
        The parsetable method attempts to guess the type of table and return the best fit data to the purpose
        """
        #Wikipedia has three types of tables to describe movies
        #wikitable which can describe the movies or the ranking of the movies
        #wikitable javascript-sorter which can describe the
        #pdb.set_trace()
        counter=0
        spanning=False
        rows=table.xpath('.//tr')
        aMovies=[]
        aHeaders=[]
        for r in rows:
                if counter==0:
                        aHeaders=r.xpath('.//th')
                        #print "Header has ",len(aHeaders),"columns"
                        raHeaders=list(reversed(aHeaders))
                        iOpeningXpath=1
                        if aHeaders:
                                spanning=checkSpanning(aHeaders[0])
                        next
                counter=counter+1
                dMovie={}
                #print "Row:",r.text_content()
                cols=r.xpath('.//td')
                rCols=list(reversed(cols))
                #print "Row :",r.text_content()," has ",len(cols),"no. of cols:"
                if spanning==True:
                        iRange=min(len(cols),len(raHeaders))
                        for i in range(0,iRange):
                                #print "Mapping :",raHeaders[i].text_content()," to ",rCols[i].text_content()
                                if isTitle(raHeaders[i]):
                                        dMovie['link']=makeLink(rCols[i])
                                dMovie[raHeaders[i].text_content()]=rCols[i].text_content()
                                dMovie['Opening']=str(year)
                else:
                        for i in range(0,len(cols)):
                                #pdb.set_trace()
                                #print [h.text_content() for h in aHeaders]
                                #print i
                                if isTitle(aHeaders[i]):
                                        dMovie['link']=makeLink(cols[i])
                                dMovie[aHeaders[i].text_content()]=cols[i].text_content()
                #print dMovie
                if dMovie:
                        aMovies.append(dMovie)
        return aMovies


def makeAMovie(dMovie,year):
        #If the movie string begins with a \n remove all text right upto the next \n"
        #Using get to avoid no link being present and key zero
        #print dMovie.get('Opening')
        sTitle=''
        oYear=oDate=oMonth=''
        if dMovie.get('Title'):
                sTitle=dMovie['Title']
        elif dMovie.get('Name'):
                sTitle=dMovie['Name']
        if dMovie.get('Opening')==str(year):
                oYear=year
                oDate=''
                oMonth=''
        elif dMovie.get('Opening'):
                sOpening=dMovie.get('Opening')
                sOpening=sOpening.strip('0'*8)
                oYear=sOpening[0:4]
                oMonth=sOpening[5:7]
                oDate=sOpening[8:10]
                #print dMovie['Opening']
        else:
                oYear=year
                oDate=''
                oMonth=''
        m=Movie(title=sTitle,director=dMovie.get('Director'),genre=dMovie.get('Genre'),
                odate=oDate,oyear=oYear,omonth=oMonth,link=dMovie.get('link')
                )
        return m
                
def filterTable(t):
    if t.attrib.has_key('class')==False:
        return False
    elif t.attrib['class']=='wikitable':
        return True
    elif t.attrib['class']=='wikitable sortable':
        return True
    else:
        return False

        
def filterTables(atTables):
        # Wikipedia has 2 formats of tables for all bollywood movies
        #2007 onwards they are in a table whose class is wikitable sortable
        #prior to that they are in a basic wikitable
        return [t for  t in atTables if filterTable(t)]


def getTablesOfMovies(year,prefix):
        url=prefix+str(year)
        pMovies=requests.get(url)
        tPage=html.fromstring(pMovies.content)
        atTables=tPage.xpath('//table')
        return filterTables(atTables)
        
def populateMovies(startyear,endyear):
        session=sMakeASession('bolytics.sqlite3')
        for z in tqdm(range(startyear,endyear)):
                #print "Parsing year:",z
                atMovies=getTablesOfMovies(z,sPagePrefix)
                for x in range(0,len(atMovies)):
                        #print "Parsing table:" ,x+1
                        table=atMovies[x]
                        if z in range(1940,1970) and x==0:
                                #print "Skipping the top grosser table for:",z 
                                #Skip the top-grossing table
                                continue
                        adMovies=parseTable(table,z)
                        #print headers
                        for y in range(0,len(adMovies)):
                                #sMovie=asMovies[y
                                movie=makeAMovie(adMovies[y],z)
                                #print "Parsing movie no.:",y
                                #print "Movie is: ",movie
                                if movie:
                                        session.add(movie)
                                session.commit()


             
sPagePrefix="https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_"


	
