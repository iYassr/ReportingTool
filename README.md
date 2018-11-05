# Newspaper Reporting Tool

██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║   ██║██╔██╗ ██║██║  ███╗       ██║   ██║   ██║██║   ██║██║     
██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██║██║╚██╗██║██║   ██║       ██║   ██║   ██║██║   ██║██║     
██║  ██║███████╗██║     ╚██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                                                               


This tool analysis a database with over 12 million row and provides a set of usable results.  

## Getting Started

Following these instuctions will get you the Newspapwer Reporting Tool up and running. 

### Prerequesite

- Vagrant image with psql up and running
- psycopg2 lib for python

```pip3 install psycopg2```  

### Coding Style

pip8

### Installation and Running

as simple as:
```python3 main.py```

### Usage

``` 
python3 main.py
---------------------------------------
The 3 Most Populer Articles of All Time

Candidate is jerk, alleges rival    --- 338647      Views
Bears love berries, alleges bear    --- 253801      Views
Bad things gone, say good people    --- 170098      Views

---------------------------------------
The Most Populer Authers of All Time

Candidate is jerk, alleges rival    --- 338647      Views
Bears love berries, alleges bear    --- 253801      Views
Bad things gone, say good people    --- 170098      Views

---------------------------------------
Days were Errors > 1%

No Results

```

## Design

an effort was made to make this tool as simple as possible.
| Function | Descreption |
| get_most_populer_articles() | returns curser with the 3 most populer articles as tuple (name, number of views) |
| get_most_populer_authors() | returns curser with most populer authors as tuple (name, number of views) |
| get_errors() | return curser with days with > %1 HTTP 404 Page not found Error (day, % of errors if  > 1 ) |
| to_print() | to print results of the query in a human-readable way  |  

### Views

get_most_populer_articles()
```
CREATE VIEW get_most_popular_articles as select articles.title, sum(stats.hits) from articles,
    (select substr(log.path,10,50) as article_name, count(*) as hits from log
    where path like '/article/%' group by path order by hits DESC) as stats
    where articles.slug = stats.article_name group by articles.title
    order by sum DESC LIMIT 3;
```

get_most_popular_authors()
```
CREATE VIEW get_most_popular_authors as select authors.name, top_authors.sum from authors,
     (select articles.author, sum(stats.hits) from articles,
      (select substr(log.path,10,50) as article_name,
      count(*) as hits from log where path like '/article/%'
       group by path order by hits DESC) as stats
       where articles.slug = stats.article_name group by articles.author
       order by sum DESC) AS top_authors
       where authors.id = top_authors.author;
```

get_errors()

```
CREATE VIEW get_errors as select found.date_trunc, (not_found.count /
    (found.count::numeric)) as error_per
    from  (select DATE_TRUNC('day', time), count(*) from log
    where status like '4%'
    group by DATE_TRUNC('day', time) order by count DESC) as not_found,
    (select DATE_TRUNC('day', time), count(*) from log
     where status not like '4%'
     group by DATE_TRUNC('day', time) order by count DESC) as found
     where found.date_trunc = not_found.date_trunc
     and (not_found.count / (found.count::numeric)) > 1;
```

## Author

iYassr

## Acknowledgment

Thanks MiSK and Udacity for this amazing course.