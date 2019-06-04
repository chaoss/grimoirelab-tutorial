# Producing Kibana dashboards with GrimoireELK

[GrimoireELK](http://github.com/chaoss/grimoirelab-elk)
is an interim system oriented to produce Kibana-based dashboards with Perceval and friends.
It provides a Python module (`grimoire_elk`) with facilities for driving
Perceval, enriching data, and uploading / downloading it to / from ElasticSearch. It includes as well some scripts (mainly `p2o.py`) to retrieve data from repositories related to software development, and produce everything needed to have Elsticsearch indexes that provide the data for a nice Kibiter/Kibana dashboard.

In summary, `p2o.py`:

* drives Perceval to retrieve data from repositories,
* uploads the resulting data as raw indexes (collections of JSON documents) to ElasticSearch
* enriches those raw indexes (produce new data with fields suitable to be used by Kibana dashboards)
* uploads that resulting data as enriched indexes to ElasticSearch

In addition, `kidash`,
available in the Python package of the same name,
can upload dashboard definitions (including visualizations, searches and everything needed by them) to produce a Kibiter/Kibana dashboards.

In this chapter we will explore how to use these tools to produce complete
Kibiter/Kibana-based dashboards.
Before following to the rest of the chapter, ensure that both
`grimoire-elk` and `kidash` Python packages are installed
(see [Installing GrimoireLab](../basics/install.html)).
