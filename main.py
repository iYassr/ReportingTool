#! /usr/env/python3
import psycopg2
import logging

'''
Log Analysis Project
@yasserd99@gmail.com
'''
# set logging to DEBUG mode
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
db = ''

# connect to db names news
try:
    db = psycopg2.connect(dbname='news')
except Exception:
    logging.exception(Exception)


def get_most_populer_articles():
    """ returns curser with the 3 most populer articles
     (name, number of views) """

    query = 'select * from most_populer_articles;'
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def get_most_populer_authors():
    """ returns curser with most populer authors (name, number of views) """
    query = 'select * from most_populer_authors;'
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def get_most_errors():
    """ return curser with days with > %1 HTTP 404 Page not found Error
    (day, % of errors if  > 1 )
    """
    query = 'select * from most_errors;'
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def to_print(curser, intro, suffex):
    """ to print results of the query in a human-readable way"""

    print('\n---------------------------------------')
    print('{} \n'.format(intro))

    if curser.rowcount == 0:
        print('No Results')
        return

    for record in curser:
        print(
            '{} --- {} {}'.format(str(record[0]).ljust(35),
                                  str(record[1]).ljust(10), suffex))


def main():
    intro = {'articles': 'The 3 Most Populer Articles of All Time',
             'authors': 'The Most Populer Authers of All Time',
             'errors': 'Days were Errors > 1%'}

    to_print(get_most_populer_articles(), intro['articles'], suffex=' Views')
    to_print(get_most_populer_authors(), intro['authors'], ' Views')
    to_print(get_most_errors(), intro['errors'], '% Errors')


main()
