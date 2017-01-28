import os
import sys
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Movie(Base):
	__tablename__='movies'
	id=Column(Integer,primary_key='True') 
	odate=Column(String)
	omonth=Column(String)
	oyear=Column(String)
	title=Column(String)
	link=Column(String)
	genre=Column(String)
	director=Column(String)
	def __str__(self):
                sSelf="<<Created on: "+str(self.odate)+"-"+str(self.omonth)+"-"+str(self.oyear)+","
                sSelf=sSelf+"Title:"+str(self.title)+","
                sSelf=sSelf+"Link:"+str(self.link)+","
                sSelf=sSelf+"Genre:"+str(self.genre)+","
                sSelf=sSelf+"Director:"+str(self.director)+">>"
                return sSelf

class Actor(Base):
	__tablename__='actors'
	id=Column(Integer,primary_key='True')
	name=Column(String)

class Character(Base):
	__tablename__='characters'
	id=Column(Integer,primary_key='True')
	name=Column(String)
	movie=Column(Integer,ForeignKey('movies.id'))
	played_by=Column(Integer,ForeignKey('actors.id'))

try:
	engine=create_engine('sqlite:///bolytics.sqlite3',echo=True)
	Base.metadata.create_all(engine)
except:
	print "Unexpected error:",sys.exc_info()[0]
	raise
