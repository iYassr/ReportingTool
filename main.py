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


def get_results(query):
    db, cursor = db_connect()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def to_print(cursor, intro, suffex):
    """ to print results of the query in a human-readable way"""

    print('\n---------------------------------------')
    print('{} \n'.format(intro))

    for record in cursor:
        print(
            '{} --- {} {}'.format(str(record[0]).ljust(35),
                                  str(record[1]).ljust(10), suffex))


if __name__ == '__main__':
    intro = {'articles': 'The 3 Most Popular Articles of All Time',
             'authors': 'The Most Popular Authers of All Time',
             'errors': 'Days were Errors > 1%'}
    query = {'articles': 'select * from most_popular_articles;',
             'authors': 'select * from most_popular_authors;',
             'errors': 'select * from most_errors;'}

    to_print(get_results(query['articles']),
             intro['articles'], suffex=' Views')
    to_print(get_results(query['authors']), intro['authors'], ' Views')
    to_print(get_results(query['errors']), intro['errors'], '%')
