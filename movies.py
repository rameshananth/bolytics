import requests
from lxml import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Movie


#setup the db session
engine=create_engine('sqlite:///bolytics',echo=True)
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

"""
Wikipedia has 2 formats for bollywood movies 1920-2007
One table with the column headers Title, Director, Cast, Genre
208 onwards there are multiple formats
"""

aiF1Years=range(1920,2007)
aiF1Years.reverse()
aiF2Years=range(2007,2016)
aiF2Years.reverse()
sPagePrefix="https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_"
x=1970
for x in aiF1Years:
	pMovies=requests.get(sPagePrefix+str(x))
	tPage=html.fromstring(pMovies.content)
	taTable=tPage.xpath('//table[@class="wikitable"]')
	tTable=taTable[0] #Because tere is always only one table
	aTitles=tTable.xpath('//td[1]/i/a/text()')
	aLink=tTable.xpath('//td[1]/i/a/@href')
	aDirector=tTable.xpath('//td[2]/text()|//td[2]/a/text()')
	aGenre=tTable.xpath('//td[4]/text()')
	aMovies=zip(['']*len(aTitles),['']*len(aTitles),[x]*len(aTitles), aTitles,aLink,aDirector,aGenre)
	for x in aMovies:
		movie=Movie(odate=x[0],omonth=x[1],oyear=x[2],title=x[3],link=x[4],director=x[5],genre=x[6])
		session.add(movie)
		session.commit()


	
