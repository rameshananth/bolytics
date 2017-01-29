#Description

This project will build a sqlite database of all Bollywood movies from 1920 onwards till the current year based on the List of Bollywood movies page found on [Wikipedia](https://en.wikipedia.org/List_of_Bollywood_movies)

Users can then analyze the database with their favourite graphing software

If you don't know what Bollywood is look [here] (https://en.wikipedia.org/Bollywood)

##Dependencies
 -lxml **On windows you may have to install through the binary**
 -sqlalchemy
 -tqdm

##Usage
###Create database
`main.py createdatabase -db=path_to_db`
###Get all bollywood movies into database
`main.py getmovies -start=startingyear -end=endingyear`
###Get all actors and characters for movies in database
`main.py genactandchars -db=path_to_db`
###Do all the above
`main.py createall`

##Limitations
-Cannot create opening date if the date spans multiple columns