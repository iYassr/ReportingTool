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


# connect to db, database name is news by default
def db_connect(database_name='news'):
    """ connects to db and return db,cursor """
    try:
        db = psycopg2.connect(dbname=database_name)
        cursor = db.cursor()
        return db, cursor

    except Exception:
        logging.exception(Exception)


def get_most_populer_articles():
    """ returns cursor with the 3 most popular articles
     (name, number of views) """

    db, cursor = db_connect()
    query = 'select * from most_popular_articles;'
    cursor.execute(query)
    return db, cursor


def get_most_populer_authors():
    """ returns cursor with most popular authors (name, number of views) """

    db, cursor = db_connect()
    query = 'select * from most_popular_authors;'
    cursor.execute(query)
    return db, cursor


def get_most_errors():
    """ return cursor with days with > %1 HTTP 404 Page not found Error
    (day, % of errors if  > 1 )
    """

    db, cursor = db_connect()
    query = 'select * from most_errors;'
    cursor.execute(query)
    return db, cursor


def to_print(db, cursor, intro, suffex):
    """ to print results of the query in a human-readable way"""

    print('\n---------------------------------------')
    print('{} \n'.format(intro))

    if cursor.rowcount == 0:
        print('No Results')
        return

    for record in cursor:
        print(
            '{} --- {} {}'.format(str(record[0]).ljust(35),
                                  str(record[1]).ljust(10), suffex))
    cursor.close()
    db.close()


if __name__ == '__main__':
    intro = {'articles': 'The 3 Most Popular Articles of All Time',
             'authors': 'The Most Popular Authers of All Time',
             'errors': 'Days were Errors > 1%'}

    db, cursor = get_most_populer_articles()
    to_print(db, cursor, intro['articles'], suffex=' Views')

    db, cursor = get_most_populer_authors()
    to_print(db, cursor, intro['authors'], ' Views')

    db, cursor = get_most_errors()
    to_print(db, cursor, intro['errors'], '%')
