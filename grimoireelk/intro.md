# Producing Kibana dashboards with GrimoireELK

[GrimoireELK](http://github.com/grimoirelab/GrimoireELK) is an interim system oriented to produce Kibana-based dashboards with Perceval and friends. It provides a Python module (`grimoire_elk`) with facilities for driving Perceval, enriching data, and uploading / downloading it to / from ElasticSearch. It includes as well some scripts (mainly `p2o.py` and `kidash.py`) to retrieve data from repositories related to software development, and produce everything needed to have a nice Kibana-based dashboard for it.

In summary, `p2o.py`:

* drives Perceval to retrieve data from repositories,
* uploads the resulting data as raw indexes (collections of JSON documents) to ElasticSearch
* enrichs those raw indexes (produce new data with fields suitable to be used by Kibana dashboards)
* uploads that resulting data as enriched indexes to ElasticSearch

In addition, `kidash.py`:

* uploads dashboard definitions (including visualizations, searches and everything needed by them) to produce a Kibana dashboard

In this chapter we will explore how to use these tools to produce complete Kibana-based dashboards.




