# Persistent storage in ElasticSearch

The data produced by Perceval can be stored in persistent storage. For example, it can be uploaded to (and later retrieved from) a database. In this section we'll learn to do it with ElasticSearch.

```bash
(perceval) $ pip install elasticsearch
```

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