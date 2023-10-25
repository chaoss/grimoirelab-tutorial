---
layout: default
title: Persistent storage in ElasticSearch
nav_order: 3
parent: Python scripting
has_children: false
has_toc: false
---


# Persistent storage in ElasticSearch

The data produced by Perceval can be stored in persistent storage. For example, it can be uploaded to (and later retrieved from) a database. In this section we'll learn to do it with ElasticSearch.

ElasticSearch provides a REST API, which we will use to upload data, and later retrieve it. It works by marshalling data as JSON documents, using HTTP for communication with the ElasticSearch server, You can find details about the API in the [ElasticSearch Reference manual](https://www.elastic.co/guide/en/elasticsearch/reference/current/).

Therefore, data in ElasticSearch can be managed with simple tools, such as [curl](https://curl.haxx.se/), or browser plugins, such as [Sense for Chrome](https://github.com/bleskes/sense). In fact, we will use `curl` occasionally, for checks and the like, later in this text. But the focus now is how to use Python scripts to access ElasticSearch. We could just use the combination of some Python HTTP module (such as [urllib](https://docs.python.org/3/library/urllib.html) or [Requests](http://docs.python-requests.org/en/master/)), and the [json](https://docs.python.org/3/library/json.html)  module.

Instead of that, we will move one abstraction layer up, and will use the [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/) module. It provides comfortable access to the primitives in the ElasticSearch REST API as convenient Python constructs. If you are interested, you could even more yet another layer up, and use the [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/) module, which provides ORM-like constructs for accessing ElasticSearch from Python. But we're not covering it here.

## Creating our first index

So, let's start with the basics of using the `elasticsearch` module. To begin with, we will add the module to our virtual environment, using pip:

```bash
pip install elasticsearch
```

Now we can write some Python code to test it
[perceval_elasticsearch_1.py](scripts/perceval_elasticsearch_1.py):

```python
from perceval.backends.core.git import Git
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
repo = Git(uri=repo_url, gitpath=repo_dir)
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
python perceval_elasticsearch_1.py
{'hash': 'dc78c254e464ff334892e0448a23e4cfbfc637a3'}
{'hash': '57bc204822832a6c23ac7883e5392f4da6f4ca37'}
{'hash': '2355d18310d8e15c8e5d44f688d757df33b0e4be'}
...
```

Once you run the script, the `commits` index is created in ElasticSearch. You can check its characteristics using `curl`. The `pretty` option is to obtain a human-readable JSON document as response. Notice that we don't need to run `curl` from the virtual environment:

```bash
curl -XGET http://localhost:9200/commits?pretty
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

## Deleting is important as well

If you want to delete the index (for example, to run the script once again) you can just run `DELETE` on its url. For example, with `curl`:

```bash
curl -XDELETE http://localhost:9200/commits
{"acknowledged":true}
```

If you don't do this, before running the previous script once again, you'll see an exception such as:

```bash
...
  File "/home/jgb/venvs/perceval/lib/python3.5/site-packages/elasticsearch/connection/base.py", line 113, in _raise_error
    raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)
elasticsearch.exceptions.RequestError: TransportError(400, 'index_already_exists_exception', 'already exists')
```

The exception is due to the `es.indices.create` line in the script, which fails because the index already exists.

If you want to avoid that problem, by deleting the index if the creation fails
(and re-creating it again),
you can just modify that line in the script with the folliwing code
(see the complete example in
[perceval_elasticsearch_2.py](scripts/perceval_elasticsearch_2.py)):

```python
# Create the 'commits' index in ElasticSearch
# if it already exisits, first delete it and then create it.
try:
    es.indices.create('commits')
except elasticsearch.exceptions.RequestError:
    es.indices.delete('commits')
    es.indices.create('commits')
```

Be careful with this code: it will delete the specified index without doubting
about it a single second.

You can check out the [cleanup.py](scripts/cleanup.py)
which deletes a list of indices, and then checks that they were actually deleted.

## A more complete index for git metadata

Let's produce now a more complete ElasticSearch index for git metadata. For each commit, it will have fields for hash, author, committer, author date and committer date (see the complete example in 
[perceval_elasticsearch_3.py](scripts/perceval_elasticsearch_3.py)):

```python
from perceval.backends.core.git import Git
import elasticsearch

# Url for the git repo to analyze
repo_url = 'http://github.com/grimoirelab/perceval.git'
# Directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'
# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Create the 'commits' index in ElasticSearch
try:
    es.indices.create('commits')
except elasticsearch.exceptions.RequestError:
    print('Index already exisits, remove it before running this script again.')
    exit()
# Create a Git object, pointing to repo_url, using repo_dir for cloning
repo = Git(uri=repo_url, gitpath=repo_dir)
# Fetch all commits as an iteratoir, and iterate it uploading to ElasticSearch
print('Analyzing git repo...')
for commit in repo.fetch():
    # Create the object (dictionary) to upload to ElasticSearch
    summary = {
        'hash': commit['data']['commit'],
        'author': commit['data']['Author'],
        'author_date': commit['data']['AuthorDate'],
        'commit': commit['data']['Commit'],
        'commit_date': commit['data']['CommitDate'],
        'files_no': len(commit['data']['files'])
        }
    print('.', end='')
    # Upload the object to ElasticSearch
    es.index(index='commits', doc_type='summary', body=summary)

print('\nCreated new index with commits.')
```

After running it (deleting any previous `commits` index if needed), we have a new index with the intended information for all commits. We can see one of them querying the index using directly the ElasticSearch REST API with `curl`:

```bash
curl -XGET "http://localhost:9200/commits/_search/?size=1&pretty"
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 407,
    "max_score" : 1.0,
    "hits" : [ {
      "_index" : "commits",
      "_type" : "summary",
      "_id" : "AVfPp9Po5xUyv5saVPKU",
      "_score" : 1.0,
      "_source" : {
        "hash" : "d1253dd9876bb76e938a861acaceaae95241b46d",
        "commit" : "Santiago Dueñas <sduenas@bitergia.com>",
        "author" : "Santiago Dueñas <sduenas@bitergia.com>",
        "author_date" : "Wed Nov 18 10:59:52 2015 +0100",
        "files_no" : 3,
        "commit_date" : "Wed Nov 18 14:41:21 2015 +0100"
      }
    } ]
  }
}
```

Since we specified in the query we only wanted one document (`size=1`), we get a list of `hits` with a single document. But we can see also how there are a total of 407 documents (field `total` within field `hits`). For each document, we can see the information we have stored, which are the contents of `_source`.

## Having dates as dates

Every index in ElasticSearch has a 'mapping'. Mappings specify how the index is, for example in terms of data types. If we don't specify a mapping before uploading data to an index, ElasticSearch will infere the mapping from the data. Therefore, even when we created no mapping for it, we can have a look at the mapping for the recently created index:

```bash
curl -XGET "http://localhost:9200/commits/_mapping?pretty"
{
  "commits" : {
    "mappings" : {
      "summary" : {
        "properties" : {
          "author" : {
            "type" : "string"
          },
          "author_date" : {
            "type" : "string"
          },
          "commit" : {
            "type" : "string"
          },
          "commit_date" : {
            "type" : "string"
          },
          "files_no" : {
            "type" : "long"
          },
          "hash" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

There is a mapping per document type in the index. In this case, we only have `summary` documents in the `commits` index (see the line `es.index()` in the script), so we only have one entry in the `mappings` object above. In it, we can see how each field got a type: `string`for character strings, and `long` for numbers.

But we know that `author_date` and `commit_date` are not really strings. Both should be recognized as dates. Let's improve our script so that both are dates (Python `datetime` objects) before they are uploaded to ElasticSearch (see all the details in 
[perceval_elasticsearch_4.py](scripts/perceval_elasticsearch_4.py)):

```python
import datetime
...
        'author_date': datetime.datetime.strptime(commit['data']['AuthorDate'],
                                                "%a %b %d %H:%M:%S %Y %z"),
...
        'commit_date': datetime.datetime.strptime(commit['data']['CommitDate'],
                                                "%a %b %d %H:%M:%S %Y %z"),
...
```

Instead of using the character strings that we get from Perceval as values for those two fields, we first convert them to `datetime` objects. This is enough for the `elasticsearch` module to recognize as dates, and upload them as such. You can check the resulting mapping after running this new script:

```bash
curl -XGET "http://localhost:9200/commits/_mapping?pretty"
{
  "commits" : {
    "mappings" : {
      "summary" : {
        "properties" : {
          "author" : {
            "type" : "string"
          },
          "author_date" : {
            "type" : "date",
            "format" : "strict_date_optional_time||epoch_millis"
          },
          "commit" : {
            "type" : "string"
          },
          "commit_date" : {
            "type" : "date",
            "format" : "strict_date_optional_time||epoch_millis"
          },
          "files_no" : {
            "type" : "long"
          },
          "hash" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

So, now we have a more complete index for commits, and each of the fields in it have reasonable types in the ElasticSearch mapping.

## Summary

In this section you have learned the basics of storing data retrieved by Perceval in a ElasticSearch server. Although all the examples were performed with the git Peceval backend, the mechanics for using any other backed are exactly the same. Therefore, if you got everything up to here, you know how to upload any kind of data produced by Perceval to ElasticSearch.
