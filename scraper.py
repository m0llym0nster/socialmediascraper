#!/usr/bin/env/python

#imports
import requests #for http requests all parts
import re #for regular expressions second part
import pandas as pd #for dataframes third part
from bs4 import BeautifulSoup #help html parsing 4th part

import logging #not part of exercise but I wanted to try using it for best practices (I also made some mistakes and wanted this here)

#functions - I defined one for each part of the exercise so I could comment out what I don't want to run and use it for notes

def firstExercise():
    #vars
    urltarget = 'https://bradfordtuckfield.com/indexarchive20210903.html'
    pagecode = requests.get(urltarget)
    #print first 600 chars
    print("just the page")
    print(pagecode.text[0:600])
    #find something in text and print
    print("finding something")

def reExercise():
    print('playing with RE')
    #use RE
    #span gets beginning and end locations of substring e.g. (10,13)
    print(re.search('cats','i love my cats').span())
    #the + looks for 1+ characters of that letter
    print(re.search('c+a+t+s+', 'i love caaats!').span())
    #if not in string throws error -try/catch prevents it from terminating program 
    #this is not in the book, but i am trying to get better at programming
    try:
        print(re.search('dogs', 'i love caaats!').span())
    except:
        print("nothing found")

    #asterisk *  wildcard is 0+, this will work also        
    print(re.search('d*o*g*s*', 'i love caaats!').span())
    #? is 0-1 times
    print(re.search('cats?','i love my cat').span())
    #escaping meta characters
    #searches for exactly one questionmark and not 0-1 questoinmarks
    print(re.search('cats\?', 'Do you love cats?').span())
    #search for 0-1 questionmarks
    print(re.search('cats\??', 'Do you love cats').span())
    #escaping the escape character \\ for searching for backslashes
    #will fail to have span type if not raw data (also \t is interpreted as a tab so dont use that in your example rofl)
    print(re.search(r'ca\\',r'i love ca\ts').span())
    #\d any digit, \D not digit, \s space,tab,newline, \t tab, \n newline, \w alphabetic chars- letter,num,underscore
    #regular regex rules seem to apply : e.g. [a-z][A-Z][a|b]^$. (. find anything not \n newline)
    #i have done a lot of xml xsd stuff, so i have most of these memorized. The real difficulty is know what nuances the regex interpreter will like.

def finditerexercise():
    #define logger here - pull in global options for logger becauuse I want to print the error from connection string
    #this is added in
    logger=logging.getLogger()
    #using finditer instead of .search because finditer finds more than one match
    urltoget = 'https://bradfordtuckfield.com/contactscrape2.html'
    try:
        pagecode = requests.get(urltoget)
        allmatches = re.finditer('[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+',pagecode.text)
        #the emails on this page do not have numbers in them

        #use list for all matches
        alladdresses= []
        for match in allmatches:
            alladdresses.append(match[0])
        print(alladdresses)

        #convert list to dataframe with pandas
        #dataframes are way better for holding large amounts of data
        #pandas is two dimensional data and labels - like an excel spreadsheet
        alladdpd=pd.DataFrame(alladdresses)
        print(alladdpd)
        #sort and export
        alladdpd=alladdpd.sort_values(0,ascending=False)
        alladdpd.to_csv('scrapertest1.csv') #would be cool to do something polymorphic here and track number of tests

    except requests.exceptions.ConnectionError as err:
        print("connection error, you probbaly misspelled the website name...ask me how i know")
        logger.debug(err)

def prettiestsoup():
    #use beautifulsoup to search for html elements/tags without complex regex
    URL='https://bradfordtuckfield.com/indexarchive20210903.html'
    response=requests.get(URL)
    #lxml is a library for processing xml and html in python
    soup=BeautifulSoup(response.text, 'lxml')
    #find_all is soup function where it finds all of the <a> tags (anchor elemnts) that hold URLS in href
    all_urls = soup.find_all('a')
    for each in all_urls:
        print(each['href'])


def main():
    #setup logging
    logger=logging.getLogger(__name__)
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.ERROR)

#comment out the exercises you dont need to run right now
#    firstExercise()
#    reExercise()
#    finditerexercise()
    prettiestsoup()

#tell it to run main
if __name__ == '__main__':
    main()

