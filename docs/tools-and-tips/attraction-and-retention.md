---
layout: default
title: Attraction & retention
nav_order: 2
parent: Tools and Tips
has_children: false
has_toc: false
---


# Attraction & retention

[ Warning: this is work in progress, use at your own risk! ]

In this section we're going to use some Python scripting, including using Pandas data frames, for producing CSV files, ElasticSearch indexes and Kibana dashboards. We will do that to study how people join and leave projects.

Some interesting data for learning about the evolution of a developing community is how people are entering and leaving it. From the point of view of the community, those are their attraction and retention rates: how they are attracting new developers, and how they are retaining (or not) active in the community over time.

For doing this analysis with GrimoireLab, we will produce an index with one entry (document) per developer, annotated with the date for the first and the last activity. The first activity will show when they started to be active. The last activity will be an indicator of whether they are still active or not: if their last activity is, say, 6 months old, it is very likely that they are no longer active members of the community.

The analysis can be done for each data source. To begin with, let's start with git. We will use a "standard" git index, such as those found in any standard GrimoireLab dashboards. So, this will be an execise of starting with some enriched GrimoireLab index, and producing a new one with specialized infomation.

But even before producing an index, we're going to just produce some CSV files, with the same structure, so that we can first learn to do the analysis, and later how to manage with uploading data to ElasticSearch. In fact, the structure of the analysis is simple:

* Get the data from ElasticSearch, using a query designed to produce data tailored for our analysis.
* Store the data in a Pandas data frame.
* Shape that data frame until we have the data we want.
* Save the data frame in a CSV file (or later, in an ElasticSearch index).

Scripts and JSON files mentioned here are available from the [tools&tips directory in the GitHub repo](https://github.com/jgbarah/GrimoireLab-training/tree/master/tools-and-tips/scripts).

Use the `enriched_elasticsearch_git_pandas7.py` script as follows:

```bash
./enriched_elasticsearch_git_pandas7.py \
  --es https://user:passwd@elasticsearch_url --es_index git \
  --es_out https://user:passwd@elasticsearch_url --es_index_out git_demo \
  --no_verify_certs
```

Then create in Kibana the index pattern `git_demo`, based on the index you just created, and upload to Kibana the following JSON files, which are the searches, visualizations and dashboards:

* `C_dashboard.json`
* `C_visualizations.json`
* `C_searches.json`

And point Kibana to load the dashboard `C_Git_Demo`.

## Final version of the script

The final version of this script is [enriched_elasticsearch_newcomers.py](https://github.com/jgbarah/GrimoireLab-training/tree/master/tools-and-tips/scripts/enriched_elasticsearch_newcomers.py).
