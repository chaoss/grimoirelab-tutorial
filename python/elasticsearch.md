# Persistent storage in ElasticSearch

The data produced by Perceval can be stored in persistent storage. For example, it can be uploaded to (and later retrieved from) a database. In this section we'll learn to do it with ElasticSearch.

ElasticSearch provides a REST API, which we will use to upload data, and later retrieve it. It works by marshalling data as JSON documents, using HTTP for communication with the ElasticSearch server, You can find details about the API in the [ElasticSearch Reference manual](https://www.elastic.co/guide/en/elasticsearch/reference/current/).

Therefore, data in ElasticSearch can be managed with simple tools, such as [curl](https://curl.haxx.se/), or browser plugins, such as [Sense for Chrome](https://github.com/bleskes/sense). In fact, we will use `curl` occasionally, for checks and the like, later in this text. But the focus now is how to use Python scripts to access ElasticSearch. We could just use the combination of some Python HTTP module (such as [urllib](https://docs.python.org/3/library/urllib.html) or [Requests](http://docs.python-requests.org/en/master/)), and the [json](https://docs.python.org/3/library/json.html)  module.

Instead of that, we will move one abstraction layer up, and will use the [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/) module. It provides comfortable access to the primitives in the ElasticSearch REST API as convenient Python constructs. If you are interested, you could even more yet another layer up, and use the [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/) module, which provides ORM-like constructs for accessing ElasticSearch from Python. But we're not covering it here.

So, let's start with the basics of using the `elasticsearch` module. To begin with, we will add the module to our virtual environment, using pip:

```bash
(perceval) $ pip install elasticsearch
```

Now we can write some Python code to test it [perceval_elasticsearch_1.py](https://github.com/jgbarah/GrimoireLab-training/blob/master/python/scripts/perceval_elasticsearch_1.py):

```python
import perceval.backends
import elasticsearch

# Url for the git repo to analyze
repo_url = 'http://github.com/grimoirelab/perceval.git'
# Directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'
# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Create the 'commits' index in ElasticSearch
es.indices.create('commits')
# Create a Git object, pointing to repo_url, using repo_dir for cloning
repo = perceval.backends.git.Git(uri=repo_url, gitpath=repo_dir)
# Fetch all commits as an iteratoir, and iterate it uploading to ElasticSearch
for commit in repo.fetch():
    # Create the object (dictionary) to upload to ElasticSearch
    summary = {'hash': commit['data']['commit']}
    print(summary)
    # Upload the object to ElasticSearch
    es.index(index='commits', doc_type='summary', body=summary)
```

This little script assumes that we're running a local instance of ElasticSearch, which is accessible via the default url: `http://localhost:9200/` (that is, port 9200 in the local machine). The script creates a new index called `commits`, which will contain the hash for every commit in the analyzed repository (in this case, the Perceval git repository).

When running it, you'll see the objects with the hashes being printed in the screen, right before they are uploaded to ElasticSearch:

```bash
(perceval) $ python perceval_elasticsearch_1.py 
{'hash': 'dc78c254e464ff334892e0448a23e4cfbfc637a3'}
{'hash': '57bc204822832a6c23ac7883e5392f4da6f4ca37'}
{'hash': '2355d18310d8e15c8e5d44f688d757df33b0e4be'}
...
(perceval) $ curl -XGET http://localhost:9200/commits?pretty
{
  "commits" : {
    "aliases" : { },
    "mappings" : {
      "summary" : {
        "properties" : {
          "hash" : {
            "type" : "string"
          }
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1476470820231",
        "number_of_shards" : "5",
        "number_of_replicas" : "1",
        "uuid" : "7DSlRG8ZSTuE1pMboG07yg",
        "version" : {
          "created" : "2020099"
        }
      }
    },
    "warmers" : { }
  }
}
```