#! python3
import psycopg2
import logging

'''
Log analysis Project
'''

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

db = ''

try:
    db = psycopg2.connect(dbname='news')
except Exception:
    logging.exception(Exception)


def get_most_populer_articles():
    query = '''select articles.title, sum(newlog.hits) from articles, 
    (select substr(log.path,10,50) as article_name, count(*) as hits from log  
    where path like '/article/%' group by path order by hits DESC) as newlog   
    where articles.slug = newlog.article_name group by articles.title order by sum DESC;'''
    cursor = db.cursor()
    cursor.execute(query)

    print('------------------------------')
    print('The Most Populer Articles of All Time \n')
    for record in cursor:
        print('{} --- {} Views'.format(record[0], record[1]))


def get_most_populer_authors():
    query = '''select authors.name, top_authors.sum from authors, (select articles.author, sum(newlog.hits) from articles, (select substr(log.path,10,50) as article_name, count(*) as hits from log where path like '/article/%' group by path order by hits DESC) as newlog where articles.slug = newlog.article_name group by articles.author order by sum DESC) AS top_authors where authors.id = top_authors.author;'''

    cursor = db.cursor()
    cursor.execute(query)
    print('------------------------------')
    print('The Most Populer Authors of All Time \n')
    for record in cursor:
        print('{} --- {} Views'.format(record[0], record[1]))


def get_most_errors():
    query = '''  select found.date_trunc, (not_found.count / (found.count::numeric)) as error_per from  (select DATE_TRUNC('day', time), count(*) from log where status like '4%' group by DATE_TRUNC('day', time) order by count DESC) as not_found, (select DATE_TRUNC('day', time), count(*) from log where status not like '4%' group by DATE_TRUNC('day', time) order by count DESC) as found where found.date_trunc = not_found.date_trunc and (not_found.count / (found.count::numeric)) > 0.0001;
    '''
    cursor = db.cursor()
    cursor.execute(query)
    print('------------------------------')
    print('Days were errors > 1% \n')
    for record in cursor:
        print('{} --- {} Errors'.format(record[0], record[1]))


def main():
    get_most_populer_articles()
    get_most_populer_authors()
    get_most_errors()


main()
