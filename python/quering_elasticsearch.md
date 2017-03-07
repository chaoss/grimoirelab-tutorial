# Queriyng ElasticSearch

In the previous section we learned how to store Perceval data in ElasticSearch. Let's learn now how to query it. For this, we're going to use data from mailing lists. First, let's upload some messages to a fresh ElasticSearch index using the Perceval mbox backend \(script [perceval\_elasticsearch\_mbox\_1.py](https://github.com/jgbarah/GrimoireLab-training/blob/master/python/scripts/perceval_elasticsearch_mbox_1.py)\):

```python
import email.utils

from perceval.backends.core.mbox import MBox
import elasticsearch

# uri (label) for the mailing list to analyze
mbox_uri = 'http://mail-archives.apache.org/mod_mbox/httpd-announce/'
# directory for letting Perceval where mbox archives are
# you need to have the archives to analyzed there before running the script
mbox_dir = 'archives'
# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Create the 'messages' index in ElasticSearch
try:
    es.indices.create('messages')
except elasticsearch.exceptions.RequestError:
    print('Index already exisits, remove it before running this script again.')
    exit()

# create a mbox object, using mbox_uri as label, mbox_dir as directory to scan
repo = MBox(uri=mbox_uri, dirpath=mbox_dir)

# Fetch all commits as an iteratoir, and iterate it uploading to ElasticSearch
print('Analyzing mbox archives...')
# fetch all messages as an iteratoir
for message in repo.fetch():
    # Create the object (dictionary) to upload to ElasticSearch
    summary = {
        'from': message['data']['From'],
        'subject': message['data']['Subject'],
        'date': email.utils.parsedate_to_datetime(message['data']['Date'])
        }
    print('.', end='')
    # Upload the object to ElasticSearch
    es.index(index='messages', doc_type='summary', body=summary)
```

And now, let's retrieve data from this recently created index. For example, we can get the sender and the subject for each stored message \([perceval\_elasticsearch\_mbox\_2.py](https://github.com/jgbarah/GrimoireLab-training/blob/master/python/scripts/perceval_elasticsearch_mbox_2.py)\):

```python
import elasticsearch

# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Query messages index, getting all items in it
es_result = es.search(index="messages")
# Print number of messages retrieved
print("Found %d messages" % es_result['hits']['total'])
for message in es_result['hits']['hits']:
    print("Sender: %s\n    Subject: %s" %
        (message['_source']['from'], message['_source']['subject']))
```

The key is the line calling `es.search`, where we are querying EalisticSearch. Since we only specify the index, we will get the whole index as a result. In fact, we get a dictionary, whose `hits` field includes several interesting fields: `total` for the total number of documents retrieved, and `hits`, for a list of the documents retrieved.

For each of these documents, the data we uploaded is in the `_source` dictionary: we only need to retrieve the needed data from there \(in this case, `from` and `subject`\).

The next script goes a step beyond, by searching for specific items \(documents\) in the index. In this case, we will ask for items whose `from` property matches \(includes\) the string `Jim` \(see file [perceval\_elasticsearch\_mbox\_3.py](https://github.com/jgbarah/GrimoireLab-training/blob/master/python/scripts/perceval_elasticsearch_mbox_3.py)\):

```python
import elasticsearch

es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

es_result = es.search(index="messages", doc_type='summary',
                    body={"query": {"match": {"from": "Jim"}}})

print("Found %d messages" % es_result['hits']['total'])
for message in es_result['hits']['hits']:
    print("Sender: %s\n    Subject: %s" %
        (message['_source']['from'], message['_source']['subject']))
```

The difference is in the parameters for the `es.search` function, which now include an specific `doc_type` \(`summary`,the one we used when uploading the items to ElasticSearch\), and a `body`, which will be interpreted as a query.

