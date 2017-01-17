import requests
from lxml import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Movie

def sMakeASession(filename):
        #setup the db session
        engine=create_engine('sqlite:///'+filename,echo=True)
        Base.metadata.bind=engine
        DBSession=sessionmaker(bind=engine)
        session=DBSession()
        return session


def parseTable(table):
        """
        The Wikipedia page on Bollywood movies has multiple formats
        1. Predominantly wikitable with the fields being title,director, genre and cast
        2. Wikitable with the fieds also including data of release which also has variants but limited to the years (2017-2007)
        3. Wikitable with the year available in row 1 mostly in the years 1940-1950 (but why?)
        4. And a few other assorted types
        The parsetable method attempts to guess the type of table and return the best fit data to the purpose
        """
        #Wikipedia has three types of tables to describe movies
        #wikitable which can describe the movies or the ranking of the movies
        #wikitable javascript-sorter which can describe the
        sTCont=table.text_content()
        if sTCont.find('\n\n00000000')!=-1:
            sSplit='\n\n00000000'
        elif sTCont.find('\n\n')!=-1:
            sSplit='\n\n'
        else:
            #default value
            sSplit='\n\n'
        asEntries=table.text_content().split(sSplit)
        asHeaders=asEntries[0].split('\n')
        fasHeaders=[header for header in asHeaders if (header!='')]
        return fasHeaders

def makeAMovie(asMovie,asHeaders):
        for x in range(1,len(asHeaders)):
            title,director,genre,odate,omonth,oyear
            if fasHeaders[x]=='Name':
                title=asMovie[x]
            elif fasHeaders[x]=='Director':
                director=asMovie[x]
            elif fasHeaders[x]=='Genre':
                genre=asMovie[x]
            elif fasHeaders[x]=='Opening':
                oyear=asMovie[x][0:4]
                omonth=asMovie[x][5:7]
                odate=asMovie[x][8:10]
                
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
        

sPagePrefix="https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_"


	
