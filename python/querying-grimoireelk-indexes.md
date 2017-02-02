## Querying grimoire-elk indexes

As we discussed in section [A simple dashboard](../grimoireelk/a-simple-dashboard.md), for producing dashboards we can run tools that use the `grimoire-elk` Python module to produce 'enriched indexes'. Those indexes are designed to be used by Kibana visualizations, but they are also suitable for direct query. The main advantage of using these enriched indexes instead of the raw ones is that we have usually higher level data, usually closer to the data we look for most analysis. The drawback is that we don't have all the data available in the raw indexes, which in some cases mean that we miss the data we need.

But when we have the data we need in them, they are easy to query, and the fact is that they can provide a good deal of quality information. Let's see how to query them using `elasticsearch_dsl`, using as an example the git enriched index. This is the one we produced for the the git Kibana dashboard in section [A simple dashboard](../grimoireelk/a-simple-dashboard.md).

### Common code for all the examples

Before we can query the index, we need to import some modules, and declare de ElasticSearch instance we're going to use:

```
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from datetime import datetime

es = Elasticsearch(["http://127.0.0.1:9200"])
```

