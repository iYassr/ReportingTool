#! python3
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

    # original query used by view
    """ query = '''select articles.title, sum(stats.hits) from articles,
    (select substr(log.path,10,50) as article_name, count(*) as hits from log
    where path like '/article/%' group by path order by hits DESC) as stats
    where articles.slug = stats.article_name group by articles.title
    order by sum DESC LIMIT 3;''' """
    query = 'select * from most_populer_articles;'
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def get_most_populer_authors():
    """ returns curser with most populer authors (name, number of views) """

    """ query = '''select authors.name, top_authors.sum from authors,
     (select articles.author, sum(stats.hits) from articles,
      (select substr(log.path,10,50) as article_name,
      count(*) as hits from log where path like '/article/%'
       group by path order by hits DESC) as stats
       where articles.slug = stats.article_name group by articles.author
       order by sum DESC) AS top_authors
       where authors.id = top_authors.author;''' """
    query = 'select * from most_populer_authors;'
    cursor = db.cursor()
    cursor.execute(query)
    return cursor


def get_most_errors():
    """ return curser with days with > %1 HTTP 404 Page not found Error
    (day, % of errors if  > 1 )
    """

    """ query = '''  select found.date_trunc, (not_found.count /
    (found.count::numeric)) as error_per
    from  (select DATE_TRUNC('day', time), count(*) from log
    where status like '4%'
    group by DATE_TRUNC('day', time) order by count DESC) as not_found,
    (select DATE_TRUNC('day', time), count(*) from log
     where status not like '4%'
     group by DATE_TRUNC('day', time) order by count DESC) as found
     where found.date_trunc = not_found.date_trunc
     and (not_found.count / (found.count::numeric)) > 1;
    '''"""
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
