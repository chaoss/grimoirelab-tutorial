## ElasticSearch DSL

The `elasticsearch` Python module may seem good enough to query ElasticSearch via its REST API. But for using it, we need to write full JSON documents with the intended queries. And these documents may become large, complex, and a burden to maintain and understand. Here is where the [`elasticsearch_dsl` Python module](http://elasticsearch-dsl.readthedocs.io) comes to the rescue.

To install it, just use pip:

```bash
pip install elasticsearch_dsl
```

It needs the `elasticsearch` Python module to work, but you'll have it already installed, or will be pulled in via dependencies, so don't worry about it.

### Get all contents in an index

`elasticsearch_dsl` provides, among other goodies, a nice chainable API for building ElasticSearch requests (queries), and a convenient way to deal with responses. Let's start by showing a very simple example which works with the index we created for git commits in the chapter on Perceval (see the code as a file ready to run,
[perceval_elasticsearch_git_dsl.py](scripts/perceval_elasticsearch_git_dsl.py)):

```python
import elasticsearch
import elasticsearch_dsl

# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Build a DSL Search object on the 'commits' index, 'summary' document type
request = elasticsearch_dsl.Search(using=es, index='commits',
                                    doc_type='summary')

# Run the Search, using the scan interface to get all resuls
response = request.scan()
for commit in response:
    print(commit.hash, commit.author_date, commit.author)
```

After importing both modules, we create an object to connect to ElasticSearch intance, as we have always done with the `elasticsearch` module. Once we have it, new stuff enters into action. First, we create a 'request', by instantiating the `elasticsearch_dsl` `Search` class. It needs the object to connect, and the name of of the index of interest. In this case, we provide the document type as well (although that is not mandatory).

Then, we obtain a reponse by calling the `scan()` method of the request. That call will produce real requests to the ElasticSearch REST API, using the scan interface. We use the scan interface because we want all documents, and on a potentially large index, this is the best way to do it. `scan()` returns a Python generator, taking care of sending new requests to ElasticSearch when needed. This, we can just iterate over it, getting all commits in the index, and printing them.

### Get only some fields

This code can be made more efficient, by requesting only the fields we need, instead of getting all the data we have for documents in the `commits` index. For that, we can just chain a call to `source()` to the request we're using. The definition of the request is shown below (a complete script is available as
[perceval_elasticsearch_git_dsl_2.py](scripts/perceval_elasticsearch_git_dsl_2.py)):

```python
request = elasticsearch_dsl.Search(using=es, index='commits',
                                    doc_type='summary')
request = request.source(['hash', 'author_date', 'author'])
```

The result is the same, but the bandwith needed, and the stress caused on the ElasticSearch server, are lower. Of course, the more unneeded data in the documents in the index, the more gain of this technique.

### Get the last commits

DSL allows for specifying filters, order, bucketing, aggregations, and much more. And all of that is available via `elasticsearch_dsl`. For example, let's get the last 20 commits, by date of commit (for each commit, only hash, author date and author, as above). The complete script is available as

[perceval_elasticsearch_git_dsl_3.py](scripts/perceval_elasticsearch_git_dsl_3.py), and the relevant fragment is below:

```python
request = request.sort('-commit_date')
request = request.source(['hash', 'author_date', 'author'])
request = request[0:20]

# Run the Search, using the execute interface to get ordered results
response = request.execute()
for commit in response:
    print(commit.hash, commit.author_date, commit.author)
```

Now, instead of `scan()`, we use `execute()` which allows for slicing (note the line where we slice `request`), and preserves order.
