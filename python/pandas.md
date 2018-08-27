## Pandas for GrimoireLab indexes

[Pandas](http://pandas.pydata.org/) is one of the most common libraries used in data analytics with Python. It can be very useful when dealing with GrimoireLab indexes. In this section, we will explore how to create dataframes (one of the most interesting data structures provided by Pandas) from GrimoireLab indexes, and how to work with them.

## Building a dataframe from an index

To start exploring how to use Pandas with GrimoireLab, we will create a simple program that creates a couple of CSV files from information in an index ([`pandas_1_py`](scripts/pandas_1.py)).

First things first: let's import the modules we're going to need: in addition to `datetime`, we will use  `elasticsearch` and `elasticsearch_dsl` for accesing the ElasticSearch instance where our index will live, and  `Pandas`.

```python
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd
```

Then we create an object for accesing the ElasticSearch instance. In this case, we'll assume that it is running in our computer, with its REST interface available in port 9200 (the default port used by ElasticSearch). The `verify_certs` is not strictly neccesary, but maybe you'll need it if you're connecting to an ElasticSearch instance over TLS (`https`) with a bad certificate. In any case, if you don't need it you better don't use it (just remove it from the call to the `Elasticsearch` constructor).

```python
es = Elasticsearch('http://localhost:9200', verify_certs=False)
```

Now we can build the query, using the facilities provided by `elasticsearch_dsl`. The query will be on the index named `git` (which should be a GrimoireLab enriched git index). These indexes store one document per commit, with some fields such as `author_name` (name of the author of the commit) and `author_date` (date of authorship of the commit).

The query build buckets of commits, grouped by author name (field `author_name`), aggregated as first commit for each of these authors (minimum field `author_date` for all the documents in each bucker).

```python
s = Search(using=es, index='git')
s.aggs.bucket('by_authors', 'terms', field='author_name', size=10000) \
    .metric('first_commit', 'min', field='author_date')
s = s.sort("author_date")
```

Now, we can execute the query:

```python
result = s.execute()
```
Note that we have specified a size of 10,000 for the buckets, which should allow for most situations. But feel free to make it larger if you're working with a really large index.

And the moment for creating a Pandas dataframe arrived! Dataframes are somewhat like tables. In this case, were'going to have one row in that table per bucket (author), with `author_name` and `author_date` as columns.

We will first create a list with all the buckets received (`buckets`). It is just a matter of extracting the relevant parts from the results of executing the query:

```python
buckets_result = result['aggregations']['by_authors']['buckets']
buckets = []
for bucket in buckets_result:
    first_commit = bucket['first_commit']['value']/1000
    buckets.append(
        {'first_commit': datetime.utcfromtimestamp(first_commit),
        'author': bucket['key']}
        )
``` 

If this code is not clear, you can insert the following two lines right after the execution of the query. It will print the JSON document received from ElasticSearch, in all its glory.

```python
from pprint import pprint
pprint(result.to_dict())
```

It will print something something akin to:

```
{'_shards': {'failed': 0, 'successful': 5, 'total': 5},
 'aggregations': {'by_authors': {'buckets': [{'doc_count': 1345,
                                              'first_commit': {'value': 1443636916000.0,
                                                               'value_as_string': '2015-09-30T18:15:16.000Z'},
                                              'key': 'Alvaro del Castillo'},
                                             {'doc_count': 557,
                                              'first_commit': {'value': 1439921307000.0,
                                                               'value_as_string': '2015-08-18T18:08:27.000Z'},
                                              'key': 'Santiago Dueñas'},
```

Once we have the list ready, we can creat a Pandas dataframe out of it:

```python
authors = pd.DataFrame.from_records(buckets)
```

There are better and more efficient ways of creating a dataframe out of the results of a query, but maybe this one is the most clear. So, let's stick to it for now. We got our first dataframe: `authors`.

Now, we can start using the magic of Pandas. For example, we can order the dataframe (that is, the rows in the dataframe, each corresponding to one commit) as follows:

```python
authors.sort_values(by='first_commit', ascending=False, inplace=True)
```

If you want to see the nice dataframe you have, you can use again the pprint trick:

```python
pprint(authors)
```

This will produce something like:

```
                            author        first_commit
...
7       Jesus M. Gonzalez-Barahona 2015-12-31 19:16:25
0              Alvaro del Castillo 2015-09-30 18:15:16
1                  Santiago Dueñas 2015-08-18 18:08:27
```

Each line in this output corresponds to a row in the dataframe. The first column is the index (which is not in ascending order because we reordered the dataframe it by first commit.

And some more Pandas magic: let's produce a new dataframe with the number of new authors per month. In this case, each row in the dataframe will correspond to a month.

```python
by_month = authors['first_commit'] \
    .groupby([authors.first_commit.dt.year,
            authors.first_commit.dt.month]) \
    .agg('count')
```

We first select the `first_commit` column The `groupby` method will produce groups by year / month, and the `agg` method will later aggregate them, by counting the rows in each group. We can use once again the good old `pprint` trick to see the `by_month` dataframe:

```
first_commit  first_commit
2015          8               1
              9               1
              12              1
2016          2               1
              3               4
              4               1
              7               3
              11              2
2017          1               1
Name: first_commit, dtype: int64
```

And we're ready for the final fireworks: producing CSV files for both dataframes:

```python
by_month.to_csv('authors_per_month.csv')
authors.to_csv('authors_first.csv',
                columns=['first_commit', 'author'],
                index=False)
```

The `to_csv` method of dataframes just dump them in a file, using the CSV conventions. We can check the files created (`authors_per_month.csv` and `authors_first.csv`):

```
2015,8,1
2015,9,1
2015,12,1
2016,2,1
2016,3,4
2016,4,1
2016,7,3
2016,11,2
2017,1,1
```


```
...
2015-12-31 19:16:25,Jesus M. Gonzalez-Barahona
2015-09-30 18:15:16,Alvaro del Castillo
2015-08-18 18:08:27,Santiago Dueñas
```