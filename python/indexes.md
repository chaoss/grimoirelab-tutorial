## Querying grimoire-elk indexes

As we discussed in section
[A simple dashboard](../gelk/simple.html),
for producing dashboards we can run tools that use the `grimoire-elk` Python module to produce 'enriched indexes'. Those indexes are designed to be used by Kibana visualizations, but they are also suitable for direct query. The main advantage of using these enriched indexes instead of the raw ones is that we have usually higher level data, usually closer to the data we look for most analysis. The drawback is that we don't have all the data available in the raw indexes, which in some cases mean that we miss the data we need.

But when we have the data we need in them, they are easy to query, and the fact is that they can provide a good deal of quality information. Let's see how to query them using `elasticsearch_dsl`, using as an example the git enriched index. This is the one we produced for the the git Kibana dashboard in section [A simple dashboard](../gelk/simple.html).

### Common code for all the examples

Before we can query the index, we need to import some modules, and declare the ElasticSearch instance we are going to use:

```
from datetime import datetime
from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch(["http://localhost:9200"])
index = 'git'
```

The first two lines import `datetime` and `pprint`, which we will use in the examples below. Then, we have the lines for importing `elasticsearch` and `elasticsearch_dsl` modules. Finally we define the ElasticSearch instance we're going to query (change that for your instance, if different), and the name of the index. In our case, we will use the name for the enriched git index, as created in section [A simple dashboard](../grimoireelk/a-simple-dashboard.md).

You can see this code at the beginning of the file [enriched_elasticsearch_1.py](https://github.com/jgbarah/GrimoireLab-training/blob/master/python/scripts/enriched_elasticsearch_1.py), which includes the examples below ass well.

### Counting total number of commits

```python
s = Search(using=es, index=index)
total = s.count()
print("Count of total number of commits in index: ", total)
```

# Counting number of unique commits

```python
s = Search(using=es, index=index)
s.aggs.metric('commits', 'cardinality', field='hash')
unique = s.count()
print("Count of unique commits in index: ", unique)
```

# Ignoring commits touching no files

Counting number of unique commits, ignoring those touching no files.

```python
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s.aggs.metric('commits', 'cardinality', field='hash')
unique_no_empty = s.count()
print("Count of unique commits in index: ", unique_no_empty)
```

# Counting commits newer than a date

Counting number of unique commits, ignoring those touching no files, and newer than a certain date.

```python
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s = s.filter('range', author_date={'gt': datetime(2016, 7, 1)})
s.aggs.metric('commits', 'cardinality', field='hash')
unique_after = s.count()
print("Count of unique commits in index, authored later than July 1st 2016: ",
 unique_after)
```

# Grouping commits by quarter

Counting number of unique commits, ignoring those touching no files, and newer than a certain date, grouping them by quarter.

```python
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s = s.filter('range', author_date={'gt': datetime(2016, 7, 1)})
s.aggs.metric('commits', 'cardinality', field='hash')
s.aggs.bucket('histogram', 'date_histogram',
    field='author_date', interval='quarter')
by_quarter = s.execute()
print("Aggregations returned by quarter")
pprint(by_quarter.to_dict()['aggregations'])
for quarter in by_quarter.to_dict()['aggregations']['histogram']['buckets']:
    print("Unique commits for quarter starting on ",
        quarter['key_as_string'],
        ": ", quarter['doc_count'])
```        
