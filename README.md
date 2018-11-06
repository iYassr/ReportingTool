# Newspaper Reporting Tool

This tool analysis a database with over 12 million row and provides a set of usable results.  

## Getting Started

Following these instuctions will get you the Newspapwer Reporting Tool up and running. 

### Prerequesite

- Vagrant image with psql up and running
- psycopg2 lib for python

```pip3 install psycopg2```  

### Coding Style

pip8

### Installation
1-  Install VirtualBox
You can download it from here (Linux, Windows, OSX ) https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
2- install Vagrant
You can Download it from here (Linux, Windows, OSX)
https://www.vagrantup.com/downloads.html
to check if vagrant is succeffully installed, please run 
`$ vagrant --versoin` from the command line
3-  Download VM Configurations
`$ git clone https://github.com/udacity/fullstack-nanodegree-vm.git  # clone git repository 
`
4-  Download Reporting Tool Projct ( THIS )
`$ git clone https://github.com/iYassr/ReportingTool.git`
move folder 'Reporting Tool' into ' the cloned folder 'vagrant' - step 4 - 

5-  Download the database
You can find it here https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
unzip the file and move content to the cloned folder 'vagrant' - step 4 - 
6- Run Vagrant Instance and ssh to it
`
$ cd vagrant # cd to the cloned project folder
$ vagrant up # wait until finished, it might take more that few minitus
$ vagrant ssh # ssh to the already configured vm
$ cd /vagrant
`
7- import news database into postgres server
`
$ psql -d news -f newsdata.sql # create tables and import data from newsdata.sql to news db
`
8- Create used views using psql shell 
`
$ psql news # access news db from psql interactive shell
# now paste these views into your shell and press enter after each one
$ CREATE VIEW most_popular_articles as select articles.title, sum(stats.hits) from articles,
        (select substr(log.path,10,50) as article_name, count(*) as hits from log
        where path like '/article/%' group by path order by hits DESC) as stats
    where articles.slug = stats.article_name group by articles.title
    order by sum DESC LIMIT 3;
    
    
$ CREATE VIEW most_popular_authors as select authors.name, top_authors.sum from authors,
        (select articles.author, sum(stats.hits) from articles,
            (select substr(log.path,10,50) as article_name,
            count(*) as hits from log where path like '/article/%'
            group by path order by hits DESC) as stats
            where articles.slug = stats.article_name group by articles.author
            order by sum DESC) AS top_authors
        where authors.id = top_authors.author;

$ CREATE VIEW most_errors as select to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio
       from (select time::date as date,
                    count(*) as total,
                    sum((status != '200 OK')::int)::float as err
                    from log
                    group by date) as errors
       where err/total > 0.01;
       
$ \q # to exit the shell
`
### Running 
`
$ vagrant ssh               # ssh to the already initilized vagrant instance
$ cd /vagrant/ReportingTool # cd into the projct folder
$ python3 main.py           # run the program



- Install Vagrant
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
| --------------------------------------- | -------------------------------------------------------------- |
| get_most_populer_articles() | returns curser with the 3 most populer articles as tuple (name, number of views) |
| get_most_populer_authors() | returns curser with most populer authors as tuple (name, number of views) |
| get_errors() | return curser with days with > %1 HTTP 404 Page not found Error (day, % of errors if  > 1 ) |
| to_print() | to print results of the query in a human-readable way  |


### Views

get_most_populer_articles()
```
CREATE VIEW most_popular_articles as select articles.title, sum(stats.hits) from articles,
        (select substr(log.path,10,50) as article_name, count(*) as hits from log
        where path like '/article/%' group by path order by hits DESC) as stats
    where articles.slug = stats.article_name group by articles.title
    order by sum DESC LIMIT 3;
```

get_most_popular_authors()
```
CREATE VIEW most_popular_authors as select authors.name, top_authors.sum from authors,
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
CREATE VIEW most_errors as select to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio
       from (select time::date as date,
                    count(*) as total,
                    sum((status != '200 OK')::int)::float as err
                    from log
                    group by date) as errors
       where err/total > 0.01;
```

## Author

iYassr

## Acknowledgment

Thanks MiSK and Udacity for this amazing course.
